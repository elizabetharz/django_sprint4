from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    # Адрес перехода на главную страницу
    path('posts/create/', PostCreateView, name='posts_create'),
    # Адрес создания новых публикаций
    path('posts/<int:post_id>/edit/', PostUpdateView, name='edit'),
    # Адрес редактирования публикации
    path('posts/<int:post_id>/delete/', PostDeleteView, name = 'post_delete'),
    # Адрес удаления публикаций
    path('posts/<int:post_id>/', PostDetailView, name='post_detail'),
    # Адрес полной публикаци
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
    # Адрес категории публикаций
    path('posts/<int:post_id>/comment/', CommentCreateView, name='comment_create'),
    # Адрес создания комментария
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/', CommentUpdateView, name='comment_edit'),
    # Адрес редактирования комментария
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/', CommentDeleteView, name='comment_delete'),
    # Адрес удаления комментария
    path('auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form=RegistrationForm,
            success_url=reverse_lazy('pages:homepage'),
    # !Адрес переадресации в случае успешного создания пользователя
        ),
        name='registration'),
    path('profile/<slug:username>/', views.profile_form, name='profile'),
    # Адрес профиля
    path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
    # Адрес изменения профиля
    path('profile/change_password', views.change_password, name='change_password'),
    # Адрес изменения пароля
]
