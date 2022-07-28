from django.shortcuts import render

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        return render(request, "front/index.html")
    return render(request, "front/login.html")
