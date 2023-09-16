from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from .serializers import (
    UserSerializer,
    UserMeSerializer,
    SignUpSerializer,
    TokenSerializer
)
from .permission import IsAdmin
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from .utils import send_confirmation_code


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username',)
    ordering = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')


class UserMeView(APIView):
    """Вью-функция для работы с текущим пользователем."""

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data, status=HTTP_200_OK)


class SignUp(APIView):
    """Вью-функция для регистрации и подтвердения по почте."""

    permission_classes = [AllowAny]

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
