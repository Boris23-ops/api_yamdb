from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор')
)


class User(AbstractUser):
    """Кастомная модель пользователя."""
    bio = models.TextField('Биография', blank=True)
    role = models.CharField('Роль', max_length=15, choices=ROLES, default=USER)
    email = models.EmailField(
        'Почта',
        unique=True,
        error_messages={
            'unique': 'Пользователь с такой почтой уже существует.'
        }
    )
    confirmation_code = models.CharField(max_length=255, blank=True, null=True)

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR or self.is_admin
