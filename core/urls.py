from django.urls import include, path
import dj_rest_auth.registration.urls
import dj_rest_auth.urls

urlpatterns = [
    path("api/", include("todos.urls")),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("", include("front.urls")),
]
