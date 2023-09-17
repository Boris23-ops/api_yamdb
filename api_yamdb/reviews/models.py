from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from api.constants import MAX_TITLE_LENGTH

User = get_user_model()


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
        null=True,
        related_name='titles',
        on_delete=models.SET_NULL,
        blank=True
    )

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return self.name


class Review(models.Model):
    """Модель Ревью"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    text = models.CharField(
        verbose_name='Текст отзыва',
        max_length=2048
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        unique_together = ('author', 'title')
        default_related_name = 'reviews'
        ordering = ['pub_date']

    def __str__(self):
        return f'Отзыв {self.author} на {self.title.name}'


class Comment(models.Model):
    """Модель комментария"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE)
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['pub_date']
        default_related_name = 'comments'

    def __str__(self):
        return self.text[:MAX_TITLE_LENGTH]
