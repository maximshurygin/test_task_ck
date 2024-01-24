from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from user.serializers import UserSerializer, MyTokenObtainPairSerializer
from django.contrib.auth import authenticate, login as django_login, logout
from rest_framework import status


@swagger_auto_schema(
    method='post',
    operation_description="Регистрация нового пользователя",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email пользователя'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль')
        },
        required=['email', 'password']
    ),
    responses={201: openapi.Response('Пользователь успешно зарегистрирован')}
)
@api_view(['POST'])
def register_view(request):
    """
    API-эндпоинт для регистрации нового пользователя.

    Принимает POST-запрос с email и паролем пользователя, регистрирует пользователя в системе.

    Args:
        request (HttpRequest): Объект запроса, содержащий данные пользователя.

    Returns:
        Response: Статус HTTP 201 с данными пользователя, если регистрация успешна.
                  Статус HTTP 400 с информацией об ошибках, если регистрация не удалась.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    operation_description="Авторизация пользователя",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email пользователя'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Пароль')
        },
        required=['email', 'password']
    ),
    responses={200: openapi.Response('Успешная авторизация'), 401: 'Неверные учетные данные'}
)
@api_view(['POST'])
def login_view(request):
    """
    API-эндпоинт для авторизации пользователя.

    Принимает POST-запрос с email и паролем, проверяет учетные данные пользователя и выполняет вход в систему.

    Args:
        request (HttpRequest): Объект запроса с учетными данными пользователя.

    Returns:
        Response: Статус HTTP 200 с сообщением об успешной авторизации.
                  Статус HTTP 401 с сообщением об ошибке, если учетные данные неверны.
    """
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)
    if user:
        django_login(request, user)
        return Response({'message': 'Успешная авторизация'}, status=status.HTTP_200_OK)
    return Response({'message': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(
    method='post',
    operation_description="Выход пользователя из системы",
    responses={200: openapi.Response('Вы успешно вышли из системы')}
)
@api_view(['POST'])
def logout_view(request):
    """
    API-эндпоинт для выхода пользователя из системы.

    Выполняет выход пользователя из системы.

    Args:
        request (HttpRequest): Объект запроса.

    Returns:
        Response: Статус HTTP 200 с сообщением о успешном выходе из системы.
    """
    logout(request)
    return Response({"message": "Вы успешно вышли из системы"}, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Представление для получения пары токенов JWT (доступ и обновление) для аутентифицированного пользователя.

    Атрибуты:
        serializer_class (MyTokenObtainPairSerializer): Класс сериализатора для генерации JWT токенов.
    """
    serializer_class = MyTokenObtainPairSerializer
