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

    def create(self, validated_data):
        """
        Создает новый объект Contact с связанным объектом NetworkEntity.
        Извлекает ID связанной сущности NetworkEntity из валидированных данных и создает контакт, связывая его с этой сущностью.

        Аргументы:
        validated_data: Словарь валидированных данных для создания контакта.

        Возвращает:
        Созданный объект Contact.
        """
        network_entity = validated_data.pop('network_entity', None)
        if network_entity is None:
            raise serializers.ValidationError("network_entity is required")

        contact = Contact.objects.create(network_entity=network_entity, **validated_data)
        return contact

    def update(self, instance, validated_data):
        """
        Обновляет существующий объект Contact.
        Извлекает ID связанной сущности NetworkEntity из валидированных данных и обновляет контакт, связывая его с новой сущностью.

        Аргументы:
        instance: Экземпляр Contact для обновления.
        validated_data: Словарь валидированных данных для обновления контакта.

        Возвращает:
        Обновленный объект Contact.
        """
        network_entity_id = validated_data.pop('network_entity_id', None)

        if network_entity_id:
            network_entity = NetworkEntity.objects.get(id=network_entity_id)
            instance.network_entity = network_entity

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class ProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Product, используемый для конвертации данных продукта в JSON и обратно.
    Исключает поле 'network_entity', так как оно связано напрямую с сущностью NetworkEntity.
    """

    class Meta:
        model = Product
        exclude = ('network_entity',)

    def create(self, validated_data):
        """
        Создает новый объект Product с связанным объектом NetworkEntity.
        Извлекает ID связанной сущности NetworkEntity из валидированных данных и создает продукт, связывая его с этой сущностью.

        Аргументы:
        validated_data: Словарь валидированных данных для создания продукта.

        Возвращает:
        Созданный объект Product.
        """
        network_entity_id = validated_data.pop('network_entity_id', None)
        product = Product(**validated_data)

        if network_entity_id:
            network_entity = NetworkEntity.objects.get(id=network_entity_id)
            product.network_entity = network_entity

        product.save()
        return product

    def update(self, instance, validated_data):
        """
        Обновляет существующий объект Product.
        Извлекает ID связанной сущности NetworkEntity из валидированных данных и обновляет продукт, связывая его с новой сущностью.

        Аргументы:
        instance: Экземпляр Product для обновления.
        validated_data: Словарь валидированных данных для обновления продукта.

        Возвращает:
        Обновленный объект Product.
        """
        network_entity_id = validated_data.pop('network_entity_id', None)

        if network_entity_id:
            network_entity = NetworkEntity.objects.get(id=network_entity_id)
            instance.network_entity = network_entity

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


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
        exclude = ('debt',)

    def create(self, validated_data):
        """
        Создает новый объект NetworkEntity и связанные объекты Contact и Product.
        Извлекает данные для контактов и продуктов из validated_data, затем создает основную сущность.
        После создания основной сущности, создает связанные объекты Contact и Product, связывая их с созданной сущностью NetworkEntity.

        Аргументы:
        validated_data: Словарь данных, прошедших валидацию, для создания сущности NetworkEntity и связанных объектов.

        Возвращает:
        Новосозданный объект NetworkEntity с связанными объектами Contact и Product.
        """
        contact_data = validated_data.pop('contact')
        products_data = validated_data.pop('products')

        network_entity = NetworkEntity.objects.create(**validated_data)

        Contact.objects.create(network_entity=network_entity, **contact_data)

        for product_data in products_data:
            Product.objects.create(network_entity=network_entity, **product_data)

        return network_entity

    def update(self, instance, validated_data):
        """
        Обновляет существующий объект NetworkEntity и связанные с ним объекты Contact и Product.
        Извлекает данные для контактов и продуктов из validated_data, затем обновляет основную сущность.
        После обновления основной сущности, обновляет связанные объекты Contact и Product, связывая обновленные данные с существующей сущностью NetworkEntity.

        Аргументы:
        instance: Экземпляр NetworkEntity для обновления.
        validated_data: Данные, прошедшие валидацию, для обновления сущности NetworkEntity и связанных объектов.

        Возвращает:
        Обновленный объект NetworkEntity с связанными объектами Contact и Product.
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
