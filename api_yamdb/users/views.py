from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.permission import IsAdmin
from users.serializers import SignUpSerializer, TokenSerializer, UserSerializer
from users.utils import generate_and_send_confirmation_code


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
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
            serializer.is_valid(raise_exception=True)
            serializer.save(role=self.request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


class SignUp(APIView):
    """Вью-функция для регистрации и подтверждения по почте."""
    permission_classes = (AllowAny,)

    def post(self, request):
        """Обрабатывает POST-запрос для регистрации пользователя."""
        if User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email')
        ).exists():
            generate_and_send_confirmation_code(request)
            return Response(request.data, status=status.HTTP_200_OK)

        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(username=request.data.get('username'))
        generate_and_send_confirmation_code(request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """Сохраняет сериализатор с указанием роли пользователя."""
        serializer.save(role=self.request.user.role)


class Token(APIView):
    """Вьюсет для получения токена."""
    permission_classes = (AllowAny,)

    def post(self, request):
        """POST-запрос на получение JWT-токена."""
        serializer = TokenSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
