from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Доступ только для пользователей с ролью admin."""

    def has_permission(self, request, view):
        """Проверяет, имеет ли пользователь разрешение
        на выполнение запроса."""
        return (request.user.is_authenticated and request.user.is_admin)
