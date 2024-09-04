from blog.constants import MAX_POSTS_PAGE
from blog.forms import CommentForm, PostForm
from blog.mixins import AuthorMixin, BaseMixin, CommentMixin, PostMixin
from blog.models import Category, Post, User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)
from django.views.generic.edit import FormMixin


class IndexListView(BaseMixin, ListView):
    """CBV вывода постов на главную страницу."""

    template_name = 'blog/index.html'


class PostDetailView(FormMixin, DetailView):
    """CBV полной информации постов."""

    model = Post
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_object(self):
        """Функция для получения объекта post."""
        post = super().get_object()
        if post.author == self.request.user:
            return post

        return get_object_or_404(
            Post,
            id=post.id,
            is_published=True,
            category__is_published=True,
            pub_date__date__lte=timezone.now(),
        )

    def get_context_data(self, **kwargs):
        """Фунция передачи данных контекста."""
        return super().get_context_data(
            **kwargs,
            form=CommentForm(),
            comments=self.object.comments.select_related('author')
        )


class CategoryView(BaseMixin, ListView):
    """CBV страницы публикаций по категории."""

    template_name = 'blog/category.html'
    slug_url_kwarg = 'category_slug'

    def get_object(self):
        """Функция для получения объекта категории."""
        return get_object_or_404(
            Category, is_published=True, slug=self.kwargs[self.slug_url_kwarg]
        )

    def get_context_data(self, **kwargs):
        """Функция передачи данных контекста."""
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_object()
        return context

    def get_queryset(self):
        """Дополнительно фильтруем посты по категории."""
        category = self.get_object()
        return super().get_queryset().filter(category=category)


# Посты
class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    """CBV для добавления поста."""

    def form_valid(self, form):
        """Проверка валидности."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Функция для переадресации пользователя."""
        return reverse(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUpdateView(
    LoginRequiredMixin, AuthorMixin, PostMixin, UpdateView
):
    """CBV для редактирования поста."""

    def get_success_url(self):
        """Функция для переадресации пользователя."""
        return reverse(
            'blog:post_detail', kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(
    LoginRequiredMixin, AuthorMixin, PostMixin, DeleteView
):
    """CBV удаления публикации."""

    def get_context_data(self, **kwargs):
        """Фунция передачи данных контекста."""
        return super().get_context_data(
            form=PostForm(instance=self.object), **kwargs
        )

    def get_success_url(self):
        """Функция для переадресации пользователя."""
        return reverse(
            'blog:profile', args=[self.request.user.username]
        )


# Комментарии
class CommentCreateView(
    LoginRequiredMixin, CommentMixin, PostMixin, CreateView
):
    """CBV добавления комментария."""

    def get_object(self):
        """Функция для получения объекта поста."""
        self.post_obj = get_object_or_404(
            Post,
            id=self.kwargs[self.pk_url_kwarg]
        )
        return self.post_obj

    def form_valid(self, form):
        """Проверка валидности."""
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.post = self.get_object()
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


class CommentUpdateView(
    LoginRequiredMixin, AuthorMixin, CommentMixin, UpdateView
):
    """CBV для редактирования комментария."""

    pk_url_kwarg = "comment_id"
    template_name = "blog/comment.html"


class CommentDeleteView(
    LoginRequiredMixin, AuthorMixin, CommentMixin, DeleteView
):
    """CBV комментария."""

    pk_url_kwarg = "comment_id"
    template_name = "blog/comment.html"


# Профиль
class Profile(ListView):
    """CBV страницы пользователя."""

    template_name = 'blog/profile.html'
    paginate_by = MAX_POSTS_PAGE

    def get_queryset(self):
        """Метод queryset."""
        self.author = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        if self.request.user == self.author:
            return (
                Post.objects.filter(author=self.author)
                .select_related('author', 'category', 'location')
                .annotate(comment_count=Count('comments'))
                .order_by('-pub_date')
            )
        return (
            Post.objects.filter(
                author=self.author,
                is_published=True,
                pub_date__lte=timezone.now()
            )
            .select_related('author')
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )

    def get_context_data(self, **kwargs):
        """Фунция передачи данных контекста."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class EditProfile(LoginRequiredMixin, UpdateView):
    """CBV страницы изменения профиля пользователя."""

    model = User
    template_name = 'blog/user.html'
    fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )

    def get_object(self):
        """Функция для возвращения пользователя."""
        return self.request.user

    def get_success_url(self):
        """Функция для переадресации пользователя."""
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user.username})
