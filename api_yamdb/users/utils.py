from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


def generate_and_send_confirmation_code(request):
    """Генерация кода подтверждения и его отправка."""
    user = get_object_or_404(User, username=request.data.get('username'))
    send_mail(
        'Yamdb. Confirmation code',
        f'confirmation_code: {default_token_generator.make_token(user)}',
        'a@yambd.face',
        [user.email]
    )


def check_confimation_code(user, confirmation_code):
    """Проверка кода подтверждения."""
    return default_token_generator.check_token(user, confirmation_code)


def get_jwt_token(user):
    """Получение JWT токена для пользователя."""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
