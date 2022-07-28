from django.urls import include, path
from rest_framework import routers

from .views import TodoView

router = routers.DefaultRouter()
router.register("todos", TodoView, basename="todos")

urlpatterns = [path("", include(router.urls))]
