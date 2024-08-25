from blog.constants import MAX_POSTS_PAGE
from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post

from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone


# Кастомные миксины
class PostMixin:
    """Класс Mixin для постов."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class CommentMixin:
    """Класс миксин для комментариев."""

    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        """Функция для переадресации пользователя."""
        return reverse(
            'blog:post_detail', kwargs={"post_id": self.kwargs['post_id']}
        )


class AuthorMixin(UserPassesTestMixin):
    """Класс миксин для автора."""

    def test_func(self):
        """Функция для проверки автора."""
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        """Если пользователь не автор."""
        return redirect('blog:post_detail', post_id=self.kwargs['post_id'])


class BaseMixin:
    """Миксин для: главная, посты категории, посты пользователя."""

    model = Post
    paginate_by = MAX_POSTS_PAGE

    def get_queryset(self):
        """Метод queryset."""
        return (
            Post.objects.select_related(
                'location',
                'author',
                'category',
            )
            .filter(
                is_published=True,
                category__is_published=True,
                pub_date__date__lte=timezone.now(),
            )
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )
