from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.serializers import (
    UserSerializer,
    UserMeSerializer,
    SignUpSerializer,
    TokenSerializer,
)
from users.permission import IsAdmin
from users.utils import send_confirmation_code


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username',)
    ordering = ('username',)
    pagination_class = PageNumberPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        methods=["GET", "PATCH"],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path="me",
    )
    def me(self, request):
        serializer = UserSerializer(request.user)
        if request.method == "PATCH":
            if request.user.is_admin:
                serializer = UserMeSerializer(
                    request.user, data=request.data, partial=True
                )
            else:
                serializer = UserSerializer(
                    request.user, data=request.data, partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role, partial=True)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.data, status=HTTP_200_OK)


class UserMeView(APIView):
    """Вью-функция для работы с текущим пользователем."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data, status=HTTP_200_OK)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class SignUp(APIView):
    """Вью-функция для регистрации и подтвердения по почте."""

    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            username = request.data.get('username')
            email = request.data.get('email')
            user, created = User.objects.get_or_create(
                username=username,
                email=email
            )
            user.confirmation_code = default_token_generator.make_token(user)
            user.save()
            send_confirmation_code(user)
            return Response(request.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class Token(APIView):
    """Вьюсет для получения токена."""

    permission_classes = [IsAuthenticated]

    @staticmethod
    def check_confirmation_code(user, confirmation_code):
        return user.confirmation_code == confirmation_code

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data.get('confirmation_code')
        username = serializer.validated_data.get('username')
        user = get_object_or_404(User, username=username)
        if self.check_confirmation_code(user, confirmation_code):
            token = AccessToken.for_user(user)
            user.confirmation_code = None
            user.save()
            return Response({'token': f'{token}'}, status=HTTP_200_OK)
        return Response(
            {'confirmation_code': ['Код не действителен!']},
            status=HTTP_400_BAD_REQUEST,
        )
