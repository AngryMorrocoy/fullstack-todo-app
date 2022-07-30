from django.shortcuts import render, redirect

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request, "front/index.html")
    return render(request, "front/login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("index")
    return render(request, "front/register.html")
