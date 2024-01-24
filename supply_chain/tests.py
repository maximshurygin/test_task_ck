from django.test import TestCase
from .models import NetworkEntity, Contact, Product
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

    def test_create_with_network_entity_id(self):
        """
        Тестирование создания сущности с указанием ID поставщика.
        Проверяет создание новой сущности NetworkEntity с указанием валидного ID существующего поставщика.
        Удостоверяется, что созданный объект правильно ссылается на заданного поставщика.
        """
        supplier_entity = NetworkEntity.objects.create(name="Supplier Entity")

        valid_data = {
            "name": "New Test Entity",
            "supplier": supplier_entity.id,
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
        self.assertTrue(serializer.is_valid())
        created_entity = serializer.save()
        self.assertEqual(created_entity.supplier.id, supplier_entity.id)

    def test_update_with_network_entity_id(self):
        """
        Тестирование обновления сущности с изменением поставщика.
        Проверяет возможность изменения поставщика у существующей сущности NetworkEntity.
        Удостоверяется, что обновленный объект корректно ссылается на нового поставщика.
        """
        initial_entity = NetworkEntity.objects.create(name="Initial Entity")
        new_supplier_entity = NetworkEntity.objects.create(name="New Supplier Entity")

        Contact.objects.create(network_entity=initial_entity, email="initial@example.com", country="Initial Country",
                               city="Initial City", street="Initial Street", house_number="123")
        Product.objects.create(network_entity=initial_entity, name="Initial Product", model="Initial Model",
                               release_date="2022-01-01")

        update_data = {
            "name": "Updated Entity",
            "supplier": new_supplier_entity.id,
            "contact": {
                "email": "updated@example.com",
                "country": "Updated Country",
                "city": "Updated City",
                "street": "Updated Street",
                "house_number": "456"
            },
            "products": [
                {
                    "name": "Updated Product",
                    "model": "Updated Model",
                    "release_date": "2023-01-01"
                }
            ]
        }

        serializer = NetworkEntityCreateUpdateSerializer(instance=initial_entity, data=update_data)
        self.assertTrue(serializer.is_valid())
        updated_entity = serializer.save()
        self.assertEqual(updated_entity.supplier.id, new_supplier_entity.id)

    def test_create_with_invalid_network_entity_id(self):
        """
        Тестирование создания сущности с невалидным ID поставщика.
        Проверяет обработку ситуации, когда указан ID поставщика, который не существует в базе данных.
        Удостоверяется, что сериализатор возвращает ошибку валидации для поля 'supplier'.
        """
        invalid_data = {
            "name": "Test Entity with Invalid Supplier",
            "supplier": 9999,
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

        serializer = NetworkEntityCreateUpdateSerializer(data=invalid_data)
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
        self.assertIn('supplier', serializer.errors)
