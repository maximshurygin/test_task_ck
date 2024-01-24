from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Менеджер пользовательской модели, который переопределяет методы создания пользователя и суперпользователя.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Создает и возвращает пользователя с указанным адресом электронной почты и паролем.

        Args:
            email (str): Адрес электронной почты пользователя.
            password (str, optional): Пароль пользователя.
            **extra_fields: Дополнительные поля для модели пользователя.

        Returns:
            User: Созданный пользователь.

        Raises:
            ValueError: Если email не предоставлен.
        """
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Создает и возвращает суперпользователя с указанным адресом электронной почты и паролем.

        Args:
            email (str): Адрес электронной почты пользователя.
            password (str): Пароль пользователя.
            **extra_fields: Дополнительные поля для модели пользователя.

        Returns:
            User: Созданный суперпользователь.

        Raises:
            ValueError: Если заданные атрибуты не соответствуют требованиям суперпользователя.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
