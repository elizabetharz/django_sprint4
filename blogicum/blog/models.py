from django.db import models
from django.contrib.auth import get_user_model
from core.models import PublishedAndCreatedModel
from blog.constants import MAX_LENGTH_RENDER_TITLE, MAX_LENGTH_TITLE

User = get_user_model()


class Category(PublishedAndCreatedModel):
    """Модель категории."""

    title = models.CharField('Заголовок', max_length=MAX_LENGTH_TITLE)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text=('Идентификатор страницы для URL; '
                   'разрешены символы латиницы, цифры, дефис и подчёркивание.')
    )

    class Meta:
        """Метакласс."""

        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        """Строковое представление объекта."""
        return self.title[:MAX_LENGTH_RENDER_TITLE]


class Location(PublishedAndCreatedModel):
    """Модель локации."""

    name = models.CharField('Название места', max_length=MAX_LENGTH_TITLE)

    class Meta:
        """Метакласс."""

        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        """Строковое представление объекта."""
        return self.name[:MAX_LENGTH_RENDER_TITLE]


class Post(PublishedAndCreatedModel):
    """Модель поста."""

    title = models.CharField('Заголовок', max_length=MAX_LENGTH_TITLE,)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=('Если установить дату и время в будущем — '
                   'можно делать отложенные публикации.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория'
    )

    image = models.ImageField(
        upload_to='picture_posts/',
        blank=True
        )

    class Meta:
        """Метакласс."""

        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        """Строковое представление объекта."""
        return self.title[:MAX_LENGTH_RENDER_TITLE]


class Comment(models.Model):
    """Модель комментариев."""

    text = models.TextField('Комментарий')
    comment = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """Метакласс."""

        ordering = ('created_at',)
