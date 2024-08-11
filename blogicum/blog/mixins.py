from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse

from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post


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
