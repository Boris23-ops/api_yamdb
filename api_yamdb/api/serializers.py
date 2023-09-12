from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор Категории"""
    model = Category
    pass


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор Жанра"""
    model = Genre
    pass


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор Произведения"""
    model = Title
    pass


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор Ревью"""
    author = SlugRelatedField(slug_field='username', read_only=True)
    titles = serializers.PrimaryKeyRelatedField(read_only=True,)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор Комментария"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    review = serializers.PrimaryKeyRelatedField(
        queryset=Review.objects.all()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'created')
        read_only_fields = ('review',)
