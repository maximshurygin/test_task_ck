from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели User.

    Используется для сериализации и десериализации данных пользователя, включая создание новых пользователей.
    Поле 'password' является write-only для обеспечения безопасности.

    Методы:
        create(validated_data): Создает и возвращает нового пользователя с хешированным паролем.
    """

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'avatar', 'phone', 'country']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        """
        Создает нового пользователя с хешированным паролем.

        Args:
            validated_data: Данные для создания пользователя.

        Returns:
            User: Новосозданный пользователь.
        """
        user = User(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            avatar=validated_data.get('avatar'),
            phone=validated_data.get('phone'),
            country=validated_data.get('country'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Кастомизированный сериализатор для получения пары токенов JWT.

    Расширяет стандартный сериализатор TokenObtainPairSerializer, добавляя в токен JWT дополнительные поля.
    """

    @classmethod
    def get_token(cls, user):
        """
        Генерирует токен JWT для пользователя, добавляя дополнительные поля.

        Args:
            user (User): Пользователь, для которого генерируется токен.

        Returns:
            token: Токен JWT с дополнительными полями.
        """
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token
