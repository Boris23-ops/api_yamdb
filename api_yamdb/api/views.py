from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from api.filter import TitleFilter
from api.mixins import ListCreateDestroyViewSet, UpdateNotAllowedMixin
from api.permissions import IsAdminOrReadOnly, IsOwnerOrAdminOrReadOnly
from api.serializers import (
    CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer,
    TitleSaveSerializer, TitleSerializer
)
from reviews.models import Category, Genre, Review, Title


class CategoryViewSet(ListCreateDestroyViewSet):
    """Вьюсет Категории"""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyViewSet):
    """Вьюсет Жанра"""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(UpdateNotAllowedMixin, viewsets.ModelViewSet):
    """Вьюсет Произведения"""

    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    ).order_by('-rating')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = TitleFilter
    ordering_fields = ('rating',)

    def get_serializer_class(self):
        """Возвращает класс сериализатора в зависимости от действия."""
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleSaveSerializer


class ReviewViewSet(UpdateNotAllowedMixin, viewsets.ModelViewSet):
    """Вьюсет Ревью"""

    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,
                          IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """Возвращает queryset для получения ревью."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создает новое ревью."""
        serializer.save(author=self.request.user, title=self.get_title())

    def get_title(self):
        """Получает объект Title по title_id."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)


class CommentViewSet(UpdateNotAllowedMixin, viewsets.ModelViewSet):
    """Вьюсет Комментария"""

    permission_classes = (IsOwnerOrAdminOrReadOnly,
                          IsAuthenticatedOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        """Возвращает queryset для получения комментариев."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Создает новый комментарий."""
        serializer.save(
            author=self.request.user,
            review=self.get_review()
        )

    def get_review(self):
        """Получает объект ревью."""
        return get_object_or_404(
            Review, pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
