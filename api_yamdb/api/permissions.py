from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """Право доступа, позволяющее только владельцам
    или администраторам изменять объекты.
    Для остальных запросов разрешен только чтение."""

    def has_permission(self, request, view):
        """Проверяет, имеет ли пользователь разрешение
        на выполнение запроса."""
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Проверяет, имеет ли пользователь разрешение на доступ к объекту."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or (request.user.is_moderator or request.user.is_admin
                or request.user.is_staff)
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Право доступа, позволяющее только администраторам изменять объекты.
    Для остальных запросов разрешено только чтение."""

    def has_permission(self, request, view):
        """Проверяет, имеет ли пользователь разрешение
        на выполнение запроса."""
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated
            and (request.user.is_admin or request.user.is_staff)
        )

    def has_object_permission(self, request, view, obj):
        """Проверяет, имеет ли пользователь разрешение на доступ к объекту."""
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_admin or request.user.is_staff)
        )
