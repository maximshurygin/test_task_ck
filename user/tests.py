from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase
from rest_framework import status
from user.models import User


class UserRegistrationTest(APITestCase):

    def test_user_registration(self):
        """
        Тестирование успешной регистрации пользователя
        """
        data = {
            'email': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(
            '/user/register/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_invalid_registration(self):
        """
        Тестирование регистрации с некорректными данными
        """
        data = {
            'email': '',
            'password': 'testpassword'
        }
        response = self.client.post(
            '/user/register/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTest(APITestCase):

    def setUp(self):
        hashed_password = make_password('testpass')
        self.user = User.objects.create(email='login@example.com', password=hashed_password)

    def test_successful_login(self):
        """
        Тестирование успешной авторизации пользователя
        """
        data = {
            'email': 'login@example.com',
            'password': 'testpass'
        }
        response = self.client.post(
            '/user/login/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        """
        Тестирование авторизации с неверными данными
        """
        data = {
            'email': 'login@example.com',
            'password': 'wrongpass'
        }
        response = self.client.post(
            '/user/login/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserLogoutTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='testuser@example.com', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_logout(self):
        """
        Тестирование выхода пользователя из системы
        """
        response = self.client.post('/user/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
