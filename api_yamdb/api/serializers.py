from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериалтзатор Категории"""
    model = Category
    pass


class GenreSerializer(serializers.ModelSerializer):
    """Сериалтзатор Жанра"""
    model = Genre
    pass


class TitleSerializer(serializers.ModelSerializer):
    """Сериалтзатор Произведения"""
    model = Title
    pass
