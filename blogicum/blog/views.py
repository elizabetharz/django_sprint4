from django.shortcuts import get_object_or_404, redirect
from blog.constants import MAX_POSTS_PAGE
from blog.models import Category, Post, Comment, User
from blog.forms import PostForm, CommentForm
from django.views.generic import (
    CreateView, UpdateView, DeleteView, DetailView, ListView
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin, UserPassesTestMixin
)
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Count
from django.views.generic.edit import FormMixin


class IndexListView(ListView):
    """CBV вывода постов на главную страницу."""

    model = Post
    template_name = 'blog/index.html'
    paginate_by = MAX_POSTS_PAGE

    def get_queryset(self, queryset=None):
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


class CategoryView(ListView):
    """CBV страницы публикаций по категории."""

    template_name = 'blog/category.html'
    paginate_by = MAX_POSTS_PAGE

    def get_queryset(self):
        """Метод queryset."""
        return (Post.objects.filter(
            category__slug=self.kwargs['category_slug'],
            is_published=True,
            category__is_published=True,
            pub_date__date__lte=timezone.now()
            )
        )

    def get_context_data(self, **kwargs):
        """Фунция передачи данных контекста."""
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category, is_published=True, slug=self.kwargs['category_slug']
        )
        return context


# Посты
class PostMixin:
    """Класс Mixin для постов."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    """CBV для добавления поста."""

    def form_valid(self, form):
        """Проверка валидности."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Функция для переадресации пользователя."""
        return reverse_lazy(
            'blog:profile', kwargs={'username': self.request.user.username}
        )


class PostUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, PostMixin, UpdateView
):
    """CBV для редактирования поста."""

    def test_func(self):
        """Функция для проверки автора."""
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        """Если пользователь не автор."""
        return redirect('blog:post_detail', post_id=self.get_object().pk)

    def form_valid(self, form):
        """Проверка валидности."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Функция для переадресации пользователя."""
        return reverse_lazy(
            'blog:post_detail', kwargs={'post_id': self.object.pk}
        )


class PostDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, PostMixin, DeleteView
):
    """CBV удаления публикации."""

    def test_func(self):
        """Функция для проверки автора."""
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        """Если пользователь не автор."""
        return redirect('blog:post_detail', post_id=self.get_object().pk)

    def get_context_data(self, **kwargs):
        """Фунция передачи данных контекста."""
        return super().get_context_data(
            form=PostForm(instance=self.object), **kwargs
        )

    def get_success_url(self):
        """Функция для переадресации пользователя."""
        return reverse_lazy(
            'blog:profile', args=[self.request.user.username]
        )


# Комментарии
class CommentMixin:
    """Класс миксин для комментариев."""

    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        """Функция для переадресации пользователя."""
        return reverse_lazy(
            'blog:post_detail', kwargs={"post_id": self.kwargs['post_id']}
        )


class CommentCreateView(
    LoginRequiredMixin, CommentMixin, PostMixin, CreateView
):
    """CBV добавления комментария."""

    def dispatch(self, request, *args, **kwargs):
        """Функция для получения объекта поста."""
        self.post_obj = get_object_or_404(
            Post,
            id=self.kwargs[self.pk_url_kwarg]
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Проверка валидности."""
        if form.is_valid():
            form.instance.author = self.request.user
            form.instance.post = self.post_obj
        return super().form_valid(form)


class CommentUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, CommentMixin, UpdateView
):
    """CBV для редактирования комментария."""

    pk_url_kwarg = "comment_id"
    template_name = "blog/comment.html"

    def test_func(self):
        """Функция для проверки автора."""
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        """Если пользователь не автор."""
        return redirect("blog:post_detail", post_id=self.get_object().pk)


class CommentDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, CommentMixin, DeleteView
):
    """CBV комментария."""

    pk_url_kwarg = "comment_id"
    template_name = "blog/comment.html"

    def test_func(self):
        """Функция для проверки автора."""
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        """Если пользователь не автор."""
        return redirect("blog:post_detail", post_id=self.get_object().pk)


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
        return (Post.objects.filter(author=self.author.id)
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
        return reverse_lazy(
            'blog:profile',
            kwargs={'username': self.request.user.username})
