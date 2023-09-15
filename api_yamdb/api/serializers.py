from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.exceptions import NotFound, ValidationError

from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор Категории"""

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор Жанра"""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSaveSerializer(serializers.ModelSerializer):
    """Сериализатор Произведения"""

    category = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор Ревью"""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title_id = self.context['request'].parser_context['kwargs'].get(
            'title_id')
        author = self.context['request'].user
        review = Review.objects.filter(
            title__id=title_id,
            author=author
        ).exists()
        if review:
            raise ValidationError(
                detail=(f'Отзыв {author} на произведения с '
                        f'id={title_id} уже существует')
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор Комментария"""
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('review',)

    def validate(self, data):
        title_id = self.context['request'].parser_context['kwargs'].get(
            'title_id')
        if not Title.objects.filter(pk=title_id).exists():
            raise NotFound(
                detail=f'Произведения с id={title_id} не существует'
            )
        return data
