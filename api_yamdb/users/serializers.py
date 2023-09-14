from rest_framework import serializers
from users.models import User


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

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использовать имя _me_ в качестве username запрещено.'
            )

    class Meta:
        model = User
        fields = ('email', 'username')
