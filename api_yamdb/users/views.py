from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from users.models import User
from users.serializers import UserSerializer, UserMeSerializer, TokenSerializer
from users.permission import IsAdmin
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated


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
            return Response({'token': f'{token}'}, status=HTTP_200_OK)
        return Response(
            {'confirmation_code': ['Код не действителен!']},
            status=HTTP_400_BAD_REQUEST,
        )
