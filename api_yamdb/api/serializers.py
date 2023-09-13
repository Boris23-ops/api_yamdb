from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериалтзатор Категории"""

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'



class GenreSerializer(serializers.ModelSerializer):
    """Сериалтзатор Жанра"""

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    """Сериалтзатор Произведения"""
    
    class Meta:
        model = Title

