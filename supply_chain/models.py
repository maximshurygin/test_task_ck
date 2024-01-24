from django.db import models


class NetworkEntity(models.Model):
    """
    Модель для представления сущности в сети продаж электроники.
    """
    name = models.CharField(max_length=255, verbose_name='Название')
    supplier = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name='Поставщик', null=True, blank=True)
    level = models.IntegerField(editable=False, verbose_name='Уровень поставщика')
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                               verbose_name='Задолженность перед поставщиком')
    creation_time = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def calculate_level(self):
        """
        Вычисляет уровень сущности в иерархии сети на основе наличия и уровня поставщика.
        Возвращает:
        int: Уровень сущности (0, 1 или 2).
        """
        if not self.supplier:
            return 0
        elif not self.supplier.supplier:
            return 1
        else:
            return 2

    def save(self, *args, **kwargs):
        """
        Переопределенный метод сохранения. Вычисляет и задает уровень сущности перед сохранением.
        """
        self.level = self.calculate_level()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Contact(models.Model):
    """
    Модель для представления контактной информации сущности сети.
    """
    network_entity = models.OneToOneField(NetworkEntity, on_delete=models.CASCADE, related_name='contact')
    email = models.EmailField(verbose_name='Email')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=20, verbose_name='Номер дома')

    def __str__(self):
        return f"{self.house_number}, {self.street}, {self.city}, {self.country}, {self.email}"


class Product(models.Model):
    """
    Модель для представления продукта, предлагаемого сущностью сети.
    """
    network_entity = models.ForeignKey(NetworkEntity, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='Название')
    model = models.CharField(max_length=255, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода продукта на рынок')

    def __str__(self):
        return f"{self.name} {self.model} {self.release_date}"
