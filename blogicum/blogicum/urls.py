from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import include, path, reverse_lazy
from django.views.generic.edit import CreateView

handler403 = 'pages.views.csrf_failure'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.internal_server_error'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('pages/', include('pages.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserCreationForm,
            success_url=reverse_lazy('pages:index')
        ),
        name='registration'
    ),
    path('', include('blog.urls')),
]
