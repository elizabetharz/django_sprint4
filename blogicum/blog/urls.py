from django.urls import path
from blog import views


app_name = 'blog'

urlpatterns = [
    path('', views.IndexListView.as_view(), name='index'),
    # Адрес перехода на главную страницу
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    # Адрес создания новых публикаций
    path('posts/<int:post_id>/edit/', views.PostUpdateView.as_view(), name='edit_post'),
    # Адрес редактирования публикации
    path('posts/<int:post_id>/delete/', views.PostDeleteView.as_view(), name = 'delete_post'),
    # Адрес удаления публикаций
    path('posts/<int:post_id>/', views.PostDetailView.as_view(), name='post_detail'),
    # Адрес полной публикаци
    path('category/<slug:category_slug>/', views.CategoryView.as_view(),
         name='category_posts'),
    # Адрес категории публикаций
    path('posts/<int:post_id>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    # Адрес создания комментария
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/', views.CommentUpdateView.as_view(), name='edit_comment'),
    # Адрес редактирования комментария
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/', views.CommentDeleteView.as_view(), name='delete_comment'),
    # Адрес удаления комментария
    path('profile/<slug:username>/', views.Profile.as_view(), name='profile'),
    # Адрес профиля
    path('profile/edit_profile/', views.EditProfile.as_view(), name='edit_profile'),
    # Адрес изменения профиля
]
