from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from users.models import User
from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    class Meta:
        model = User
        fields = '__all__'


class UserMeSerializer(UserSerializer):
    """Сериализатор для текущего пользователя."""

    role = serializers.CharField(read_only=True)


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации."""

    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+$')]
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено."
            )

    class Meta:
        model = User
        fields = ('id', 'email', 'username')


class TokenSerializer(serializers.ModelSerializer):
    """Cериалайзер для получения токена."""

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            UnicodeUsernameValidator,
        ],
    )
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
