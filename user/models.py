from django.contrib.auth.models import AbstractUser
from django.db import models

from user.managers import CustomUserManager

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """
    Кастомизированная модель пользователя, расширяющая стандартную модель AbstractUser.
    Данная модель заменяет стандартное имя пользователя (username) на адрес электронной почты (email) в качестве основного идентификатора.
    Включает дополнительные поля, такие как имя, фамилия, аватар, телефон и страна.
    """

    username = None
    email = models.EmailField(unique=True, verbose_name='Почта')

    first_name = models.CharField(max_length=200, verbose_name='Имя', **NULLABLE)
    last_name = models.CharField(max_length=200, verbose_name='Фамилия', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    phone = models.CharField(max_length=35, verbose_name='Номер телефона', **NULLABLE)
    country = models.CharField(max_length=35, verbose_name='Страна', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
