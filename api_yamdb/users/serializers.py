from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.validators import UniqueTogetherValidator

from users.models import User
from users.utils import check_confimation_code, get_jwt_token


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор данных для регистрации."""

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
            raise serializers.ValidationError('Неверный код подтверждени')
        return get_jwt_token(user=user)

    def to_representation(self, instance):
        return {'token': self.get_token(instance)}


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_username(self, value):
        """Валидация уникальности имени пользователя."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                'Пользователь с таким именем уже существует.'
            )
        if value == 'me':
            raise serializers.ValidationError(
                'Недопустимое значение для роли.'
            )
        return value
