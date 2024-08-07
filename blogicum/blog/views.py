from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from blog.common import filter_objects_published
from blog.constants import MAX_POSTS_PAGE
from blog.models import Category, Post, Comment, Location
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from blog.forms import PostForm, CommentForm
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


def index(request: HttpRequest) -> HttpResponse:
    """Функция вызова шаблона (главная страница)."""
    posts = filter_objects_published(Post.objects)[:MAX_POSTS_PAGE]
    return render(request, 'blog/index.html', {'post_list': posts})


class PostDetailView(DetailView):
    """CBV полной информации постов."""

    model = Post
    form_class = PostForm
    template_name = 'blog/detail.html'
    success_url = reverse_lazy('post:list')


def category_posts(request: HttpRequest, category_slug: str) -> HttpResponse:
    """Функция вызова шаблона (категории)."""
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )
    post_list = filter_objects_published(category.posts)
    return render(request, 'blog/category.html', {
        'category': category,
        'post_list': post_list
    }
    )


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """CBV для определения админа."""

    def test_func(self):
        return self.request.user.is_staff


class CategoryCreateView(AdminRequiredMixin, CreateView):
    """CBV добавления новой категории."""

    model = Category
    success_url = reverse_lazy('category:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class LocationCreateView(AdminRequiredMixin, CreateView):
    """CBV добавления новой локации."""

    model = Location
    success_url = reverse_lazy('location:list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


def profile_form(request):
    """Страница пользователя."""
    return render(request, 'blog/profile.html')


def profile_registration(request):
    """Страница регистрации пользователя."""
    return render(request, 'registration/registration_form.html')


@login_required
def edit_profile(request):
    """Страница редактирования профиля."""
    return render(request, 'blog/user.html')


@login_required
def change_password(request):
    """Страница смены пароля."""
    return render(request, 'registration/password_change_form.html')


class IndexListView(ListView):
    """CBV пагинации главной страницы."""

    index = Post.objects.order_by('id')
    paginator = Paginator(index, 10)


class ProfileListView(ListView):
    """CBV пагинации страницы пользователей."""

    profile = Post.objects.order_by('id')
    paginator = Paginator(profile, 10)


class CategoryListView(ListView):
    """CBV пагинации страницы категорий."""

    category = Post.objects.order_by('id')
    paginator = Paginator(category, 10)


class PostListView(ListView):
    """CBV поста."""

    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    paginate_by = POST_PER_PAGE

    def get_queryset(self):
        queryset = (
            Post.objects.filter(
                is_published=True,
                category__is_published=True,
                pub_date__lte=NOW,
            )
            .annotate(comment_count=Count('comments'))
            .order_by('-pub_date')
        )
        return queryset


class PostMixin:
    """Класс Mixin для постов."""

    model = Post
    form_class = PostForm
    template_name = 'blog/create.html'
    success_url = reverse_lazy('post:list')


class PostCreateView(LoginRequiredMixin, PostMixin, CreateView):
    """CBV для добавления поста."""

    success_url = ('profile/<username>/')


class PostUpdateView(LoginRequiredMixin, PostMixin, UpdateView):
    """CBV для редактирования поста."""

    success_url = ('posts/<int:post_id>/edit')


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """CBV удаления публикации."""

    model = Post
    success_url = reverse_lazy('post:list')


class CommentMixin:
    """Класс миксин для комментариев."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    success_url = reverse_lazy('comment:list')


class CommentCreateView(LoginRequiredMixin, CommentMixin, CreateView):
    """CBV добавления комментария."""

    pass


class CommentUpdateView(LoginRequiredMixin, CommentMixin, UpdateView):
    """CBV для редактирования комментария."""

    pass


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    """CBV комментария."""

    model = Comment
    success_url = reverse_lazy('comment:list')
