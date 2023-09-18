from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import User
from .serializers import (
    TokenSerializer,
    SignUpSerializer,
    UserSerializer
)
from .permission import IsAdmin
from .utils import generate_and_send_confrimation_code


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
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request, *args, **kwargs):
        """Доступ пользователя к своему профилю."""
        self.object = User.objects.get(username=self.request.user.username)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                self.object,
                data=self.request.data,
                context={'request': self.request},
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


class SignUp(APIView):
    """Вью-функция для регистрации и подтвердения по почте."""
    permission_classes = (AllowAny,)

    def post(self, request):
        """Создание пользователя и отправка кода подтверждения."""
        serializer = SignUpSerializer(data=self.request.data)
        if serializer.is_valid():
            user = serializer.save()
            generate_and_send_confrimation_code(
                user=user,
                data=serializer.data
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )


class Token(APIView):
    """Вьюсет для получения токена."""
    permission_classes = (AllowAny,)

    def post(self, request):
        """POST-запрос на получение JWT-токена."""
        serializer = TokenSerializer(data=self.request.data)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
