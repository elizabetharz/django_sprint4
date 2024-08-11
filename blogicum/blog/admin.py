from django.contrib import admin

from blog.models import Category, Comment, Location, Post


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Класс локации."""

    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    search_fields = ('name',)
    list_editable = (
        'is_published',
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Класс поста."""

    list_display = (
        'title',
        'text',
        'is_published',
        'category',
        'pub_date',
        'created_at',
        'author',
        'location',
    )
    list_editable = (
        'category',
        'is_published',
    )
    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Класс категории."""

    list_display = (
        'title',
        'description',
        'is_published',
        'created_at',
    )
    search_fields = ('title',)
    list_editable = (
        'description',
        'is_published',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Класс комментария."""

    list_display = ["post", "author", "created_at", "short_text"]
