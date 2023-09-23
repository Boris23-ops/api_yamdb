from django.contrib import admin
from django.utils.text import format_lazy

from .models import Category, Comment, Genre, Review, Title


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'text',
        'author',
        'score',
        'pub_date'
    )
    list_editable = ('text',)
    search_fields = ('title', 'text',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'review',
        'text',
        'author',
        'pub_date'
    )
    list_editable = ('text',)
    search_fields = ('review', 'text',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')

    list_editable = ('name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'category',
    )

    list_editable = ('name', 'description', 'category', 'year')
    search_fields = ('name', 'year', 'genre', 'category')
    empty_value_display = '-пусто-'

    def get_genres_list(self, obj):
        return format_lazy(', '.join(
            [genre.name for genre in obj.genre.all()]
        ))

    get_genres_list.short_description = 'Жанры'
