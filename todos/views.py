from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Todo
from .serializers import TodoSerializer


class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Todo.objects.filter(owner=user)
