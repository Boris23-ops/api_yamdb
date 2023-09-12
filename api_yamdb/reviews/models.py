from django.db import models


class Category(models.Model):
    """Модель категории"""
    name = models.CharField(
        'Название',
        max_length=256,
        default=None
    )
    slug = models.SlugField(
        'slug',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.name


class Genre(models.Model):
    """Модель жанра"""
    name = models.CharField(
        'Название',
        max_length=100,
        default=None
    )
    slug = models.SlugField(
        'slug',
        max_length=50,
        unique=True
    )

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Модель произведения"""
    name = models.CharField(
        'Название',
        max_length=256,
    )
    year = models.IntegerField(
        'Год выпуска',

    )
    description = models.CharField(
        'Описание',
        blank=True,
        null=True,
        max_length=256
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles'
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.CASCADE,
        blank=True
    )

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.name
