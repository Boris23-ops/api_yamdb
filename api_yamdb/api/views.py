from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer
from .permissions import IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    """Вьюсет Категории"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', ]
    lookup_field = 'slug'
    pagination_class = PageNumberPagination

class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет Жанра"""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', ]
    lookup_field = 'slug'
    pagination_class = PageNumberPagination


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет Произведения"""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['name', ]
    lookup_field = 'slug'
    pagination_class = PageNumberPagination
