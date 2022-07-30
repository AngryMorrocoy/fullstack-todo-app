from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Todo


class TodoTest(APITestCase):

    list_url = reverse("todos-list")
    user_model = get_user_model()

    def get_detail_url(self, *args):
        return reverse("todos-detail", args=args)

    def test_dont_allow_unauthorized(self):
        """
        Anonymous users shouldn't be able to do any
        request related to todos
        """

        detail_url = self.get_detail_url(1)

        responses = [
            self.client.get(self.list_url),
            self.client.post(self.list_url),
            self.client.get(detail_url),
            self.client.post(detail_url),
            self.client.patch(detail_url),
            self.client.put(detail_url),
            self.client.delete(detail_url),
        ]

        for res in responses:
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_todo(self):
        """
        Authorized users should be able to create todos
        """

        user = self.user_model(username="test", password="testpass")
        user.save()

        self.client.force_authenticate(user=user)

        mock_todo = {"title": "testTodo", "owner": user.id}

        response = self.client.post(
            self.list_url, data=mock_todo, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 1)

    def test_get_todos(self):
        """
        Users should only be able to get those todos created by himself
        """
        user1 = self.user_model(username="test1", password="testpass")
        user2 = self.user_model(username="test2", password="testpass")

        user1.save()
        user2.save()

        for user in [user1, user1, user2]:
            Todo(title="testtodo", owner=user).save()

        self.client.force_authenticate(user=user1)

        response = self.client.get(self.list_url)
        todos = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(todos), 2)

        for todo in todos:
            self.assertEqual(todo["owner"], user1.id)

        self.client.force_authenticate(user=user2)

        response = self.client.get(self.get_detail_url(todos[1]["id"]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_todos(self):
        """
        Users should only be able to delete those todos created by himself
        """
        user1 = self.user_model(username="test1", password="testpass")
        user2 = self.user_model(username="test2", password="testpass")
        user1.save()
        user2.save()

        todo = Todo(title="testtodo", owner=user1)
        todo.save()

        url = self.get_detail_url(todo.id)

        self.client.force_authenticate(user=user2)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Todo.objects.count(), 1)

        self.client.force_authenticate(user=user1)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.count(), 0)

    def test_update_todos(self):
        """
        Users should be able to edit those todos of his own
        """
        user1 = self.user_model(username="test1", password="testpass")
        user2 = self.user_model(username="test2", password="testpass")
        user1.save()
        user2.save()

        todo = Todo(title="testtodo", completed=False, owner=user1)
        todo.save()
        url = self.get_detail_url(todo.id)

        new_todo = {"title": "edited", "completed": True}

        self.client.force_authenticate(user=user2)

        response = self.client.patch(url, data=new_todo, format="json")

        todo.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(todo.title, new_todo["title"])
        self.assertNotEqual(todo.completed, new_todo["title"])

        self.client.force_authenticate(user=user1)
        response = self.client.patch(url, data=new_todo, format="json")

        todo.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(todo.title, new_todo["title"])
        self.assertEqual(todo.completed, new_todo["completed"])
