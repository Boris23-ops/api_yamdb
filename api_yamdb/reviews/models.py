import datetime as dt
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .constants import MAX_SLUG_LENGTH, MAX_TEXT_LENGTH, MAX_TITLE_LENGTH


User = get_user_model()


class CommonFields(models.Model):
    """Абстрактный класс для общих полей"""

    name = models.CharField(
        'Название',
        max_length=MAX_TEXT_LENGTH,
        default=None
    )
    slug = models.SlugField(
        'slug',
        max_length=MAX_SLUG_LENGTH,
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name[:MAX_TITLE_LENGTH]


class Category(CommonFields):
    """Модель категории"""

    ...


class Genre(CommonFields):
    """Модель жанра"""

    ...


class Title(models.Model):
    """Модель произведения"""

    name = models.CharField(
        'Название',
        max_length=MAX_TEXT_LENGTH,
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
        validators=[MaxValueValidator(dt.datetime.now().year)]
    )
    description = models.CharField(
        'Описание',
        blank=True,
        null=True,
        max_length=MAX_TEXT_LENGTH
    )
    genre = models.ManyToManyField(
        Genre,
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        blank=True
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = 'Произведение'
        indexes = [
            models.Index(fields=['year']),
        ]
        ordering = ('name',)


class ComRevFilds(models.Model):
    """Абстрактный класс для общих полей"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('pub_date',)


class Review(ComRevFilds):
    """Модель Ревью"""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )

    class Meta(ComRevFilds.Meta):
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review'
            ),
        )
        default_related_name = 'reviews'
        verbose_name = 'Ревью'

    def __str__(self):
        return f'Отзыв {self.author} на {self.title}'


class Comment(ComRevFilds):
    """Модель комментария"""

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE
    )

    class Meta(ComRevFilds.Meta):
        default_related_name = 'comments'
        verbose_name = 'Комментарий'

    def __str__(self):
        return (
            f'Комментарий {self.author} на отзыв {self.review.author} '
            f'на {self.review.title}'
        )
