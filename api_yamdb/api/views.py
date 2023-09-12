from rest_framework import viewsets

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет Категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет Жанра"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет Произведения"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
