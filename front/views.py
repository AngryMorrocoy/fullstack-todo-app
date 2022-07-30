from django.shortcuts import render, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.conf import settings


def is_authenticated(request: WSGIRequest):

    jwt_cookie = settings.JWT_AUTH_COOKIE

    if jwt_cookie not in request.COOKIES:
        return False

    return request.user.is_authenticated


def index_view(request: WSGIRequest):
    if is_authenticated(request):
        return render(request, "front/index.html")
    return render(request, "front/login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    return render(request, "front/register.html")
