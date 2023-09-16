from django.core.mail import send_mail


def send_confirmation_code(user):
    """Функция для получения кода подтверждения по почте."""
    send_mail(
        'confirmation_code',
        f'confirmation_code: {user.confirmation_code}',
        'a@yambd.face',
        [user.email]
    )
