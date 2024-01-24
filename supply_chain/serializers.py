from rest_framework import serializers
from supply_chain.models import NetworkEntity, Contact, Product


class ContactSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Contact, предназначенный для преобразования данных контактов в JSON и обратно.
    Исключает поле 'network_entity' из сериализации, поскольку оно связано с основной сущностью NetworkEntity.
    """

    class Meta:
        model = Contact
        exclude = ('network_entity',)


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product, используемый для конвертации данных продукта в JSON и обратно.
    Исключает поле 'network_entity', так как оно связано напрямую с сущностью NetworkEntity.
    """

    class Meta:
        model = Product
        exclude = ('network_entity',)


class NetworkEntityListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для предоставления данных сущности NetworkEntity, включая связанные контакты и продукты.
    Используется для чтения данных, где контакт и продукты отображаются в режиме 'read_only'.
    """
    contact = ContactSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkEntity
        fields = '__all__'


class NetworkEntityCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления сущности NetworkEntity.
    Включает в себя логику для обработки связанных данных контактов и продуктов при создании или обновлении сущности NetworkEntity.
    """
    contact = ContactSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = NetworkEntity
        exclude = ('debt',)  # Исключаем поле 'debt'

    def create(self, validated_data):
        """
        Создает новую сущность NetworkEntity и связанные с ней объекты Contact и Product.
        Аргументы: validated_data: Данные, прошедшие валидацию, для создания NetworkEntity и связанных объектов.
        Возвращает: Созданный объект NetworkEntity.
        """
        contact_data = validated_data.pop('contact')
        products_data = validated_data.pop('products', [])

        contact = Contact.objects.create(**contact_data)

        network_entity = NetworkEntity.objects.create(contact=contact, **validated_data)

        for product_data in products_data:
            Product.objects.create(network_entity=network_entity, **product_data)

        return network_entity

    def update(self, instance, validated_data):
        """
        Обновляет существующий объект NetworkEntity и связанные с ним объекты Contact и Product.
        Аргументы:
        instance: Экземпляр NetworkEntity для обновления.
        validated_data: Данные, прошедшие валидацию, для обновления.
        Возвращает:
        Обновленный объект NetworkEntity.
        """
        contact_data = validated_data.pop('contact')
        products_data = validated_data.pop('products', [])

        Contact.objects.filter(id=instance.contact.id).update(**contact_data)

        for product_data in products_data:
            product_id = product_data.get('id')
            if product_id:
                Product.objects.filter(id=product_id).update(**product_data)
            else:
                Product.objects.create(network_entity=instance, **product_data)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
