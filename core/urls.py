from django.urls import include, path

urlpatterns = [
    path("api/", include("todos.urls")),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("", include("front.urls")),
]
