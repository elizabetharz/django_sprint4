from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def about(request: HttpRequest) -> HttpResponse:
    """Функция вызова шаблона (про нас)."""
    return render(request, 'pages/about.html')


def rules(request: HttpRequest) -> HttpResponse:
    """Функция вызова шаблона (наши правила)."""
    return render(request, 'pages/rules.html')


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def internal_server_error(request):
    return render(request, 'pages/505.html', status=500)