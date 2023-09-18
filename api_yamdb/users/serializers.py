from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.validators import UniqueTogetherValidator

from .models import User
from .utils import check_confimation_code, get_jwt_token
from .utils import generate_and_send_confirmation_code


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор данных для регистрации."""

    def post(self, validated_data):
        # создание пользователя
        user = User.objects.create_user(
            email=validated_data.get('email'),
            username=validated_data.get('username'),
            password=validated_data.get('password')
        )

        # генерация и отправка кода подтверждения
        code = generate_and_send_confirmation_code(user, validated_data)

        # сохранение кода подтверждения в поле confirmation_code модели User
        user.confirmation_code = code
        user.save()

        return user

    class Meta:
        model = User
        fields = ('email', 'username')

        validators = [
            UniqueTogetherValidator(
                message='Пользователь с таким email уже существует',
                queryset=User.objects.all(),
                fields=('email', 'username')
            )
        ]

    def validate_username(self, value):
        """Валидация имени пользователя."""

        if value == 'me':
            raise serializers.ValidationError(
                'Пожалуйста, не пытайтесь зарегистрировать пользователя '
                'с именем "me".')
        return value


class TokenSerializer(serializers.Serializer):
    """Cериалайзер для получения токена."""

    username = serializers.CharField()
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        """Проверка кода подтверждения и получение JWT токена."""

        username = obj['username']
        user_queryset = User.objects.filter(username=username)
        if not user_queryset.exists():
            raise NotFound(
                detail=f'Пользователя с именем {username} не существует'
            )
        user = User.objects.get(username=username)
        confirmation_code = self.initial_data.get('confirmation_code')
        if not check_confimation_code(
                user=user,
                confirmation_code=confirmation_code):
            raise serializers.ValidationError('Неверный код подтверждения')
        return get_jwt_token(user=user)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')

    def validate_role(self, value):
        """Защита от изменения своей роли пользователем без админских прав."""

        request_user = self.context.get('request').user
        if (
            value
            and request_user
            and not (request_user.is_admin or request_user.is_staff)
        ):
            return request_user.role
        return value
