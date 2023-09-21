from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import (Category, Comment, Genre, Review, Title)


class GenreInline(admin.TabularInline):
    model = Genre


class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'get_genres', 'get_categories')
    list_filter = ('genres', 'categories')
    search_fields = ('name', 'categories__name', 'genres__name')

    def get_genres(self, obj):
        return mark_safe(', '.join([genre.name for genre in obj.genres.all()]))
    get_genres.short_description = 'Жанры'

    def get_categories(self, obj):
        return mark_safe(', '.join(
            [category.name for category in obj.categories.all()]
        ))
    get_categories.short_description = 'Категории'

    inlines = [GenreInline]


admin.site.register(Category)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review)
admin.site.register(Comment)
