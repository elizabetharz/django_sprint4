from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Класс BlogConfig."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'Блог'
