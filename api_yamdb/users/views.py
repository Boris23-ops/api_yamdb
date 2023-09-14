from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from users.models import User
from users.serializers import UserSerializer, UserMeSerializer
from users.permission import IsAdmin, IsAuthenticated


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('username',)
    ordering = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')


class UserMeView(APIView):
    """Вью-функция для работы с текущим пользователем."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data, status=HTTP_200_OK)
