from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Проверка доступа: администратор."""

    message = 'Доступно только администратору.'

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsAdminOrSafeMethods(IsAdmin):
    """Проверка доступа: администратор и анонимный просмотр."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or super().has_permission(request, view)
        )


class IsAuthor(permissions.IsAuthenticatedOrReadOnly):
    """Проверка доступа: автор или модератор."""

    message = 'Доступно автору или модератору.'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
        )
