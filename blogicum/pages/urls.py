from django.urls import path

from . import views


app_name = 'pages'

urlpatterns = [
    path('about/', views.AboutPage.as_view(), name='about'),
    path('rules/', views.RulesPage.as_view(), name='rules'),

]


handler404 = 'pages.views.page_not_found'

handler500 = 'pages.views.internal_server_error'