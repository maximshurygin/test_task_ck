from django.test import TestCase
from .models import NetworkEntity
from rest_framework.test import APITestCase

from .serializers import NetworkEntityCreateUpdateSerializer


class NetworkEntityModelTest(TestCase):
    """
    Набор тестов для модели NetworkEntity.

    Тесты проверяют функциональность создания экземпляров NetworkEntity и корректность работы методов модели.
    """

    def test_create_network_entity(self):
        """
        Тест на успешное создание объекта NetworkEntity.
        Проверяет, что объект успешно сохраняется в базу данных и его имя соответствует заданному.
        """
        network_entity = NetworkEntity.objects.create(name="Test Entity")
        self.assertEqual(network_entity.name, "Test Entity")

    def test_calculate_level(self):
        """
        Тест на корректное вычисление уровня иерархии сущности (level) в NetworkEntity.
        Проверяет, что метод calculate_level правильно определяет уровень иерархии для созданных сущностей.
        """
        parent_entity = NetworkEntity.objects.create(name="Parent Entity")
        child_entity = NetworkEntity.objects.create(name="Child Entity", supplier=parent_entity)
        self.assertEqual(child_entity.calculate_level(), 1)


class NetworkEntitySerializerTest(APITestCase):
    """
    Набор тестов для сериализатора NetworkEntityCreateUpdateSerializer.

    Тесты проверяют корректность сериализации и десериализации данных, а также валидацию данных.
    """

    def test_serializer_with_valid_data(self):
        """
        Тест на успешную сериализацию с валидными данными.
        Проверяет, что сериализатор правильно обрабатывает корректные данные и не выдает ошибок валидации.
        """
        valid_data = {
            "name": "Test Entity",
            "supplier": None,
            "contact": {
                "email": "test@example.com",
                "country": "Test Country",
                "city": "Test City",
                "street": "Test Street",
                "house_number": "123"
            },
            "products": [
                {
                    "name": "Product 1",
                    "model": "Model 1",
                    "release_date": "2022-01-01"
                }
            ]
        }
        serializer = NetworkEntityCreateUpdateSerializer(data=valid_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

    def test_serializer_with_invalid_data(self):
        """
        Тест на обработку невалидных данных сериализатором.
        Проверяет, что сериализатор отвергает некорректные данные и выдает ошибки валидации.
        """
        invalid_data = {"name": ""}
        serializer = NetworkEntityCreateUpdateSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
