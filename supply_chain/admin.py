from django.contrib import admin
from .models import NetworkEntity, Product, Contact


class ProductInline(admin.TabularInline):
    """
    Встроенный класс для представления продуктов в админ-панели Django в контексте NetworkEntity.
    Позволяет отображать и редактировать связанные продукты непосредственно из формы редактирования NetworkEntity.
    """
    model = Product
    extra = 0
    verbose_name_plural = 'Продукты'


class ContactInline(admin.TabularInline):
    """
    Встроенный класс для представления контактной информации в админ-панели Django в контексте NetworkEntity.
    Позволяет отображать и редактировать контактную информацию непосредственно из формы редактирования NetworkEntity.
    """
    model = Contact
    extra = 0
    verbose_name_plural = 'Контакты'


@admin.register(NetworkEntity)
class NetworkEntityAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели NetworkEntity.

    Определяет представление списка, фильтрацию, действия и встроенные формы для управления экземплярами NetworkEntity
    в административной панели Django.
    """
    list_display = ('name', 'supplier_link', 'level', 'debt', 'creation_time')
    list_filter = ('contact__city',)
    actions = ['clear_debt']
    inlines = [ContactInline, ProductInline]

    def supplier_link(self, obj):
        """
        Возвращает ссылку на поставщика для объекта NetworkEntity.
        Args:
            obj (NetworkEntity): Экземпляр модели NetworkEntity.
        Returns:
            str: Строковое представление поставщика или '---', если поставщик отсутствует.
        """
        return obj.supplier if obj.supplier else '---'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Переопределяет поле формы для внешнего ключа 'supplier', исключая текущий объект из списка выбора.
        Args:
            db_field (Field): Поле, для которого создается форма.
            request (HttpRequest): Объект HTTP-запроса.
            **kwargs: Дополнительные параметры.
        Returns:
            Field: Поле формы для внешнего ключа.
        """
        if db_field.name == "supplier":
            kwargs["queryset"] = NetworkEntity.objects.exclude(id__exact=request.resolver_match.kwargs.get('object_id'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    supplier_link.short_description = 'Поставщик'
    supplier_link.admin_order_field = 'supplier'

    @admin.action(description='Очистить задолженность')
    def clear_debt(self, request, queryset):
        """
        Действие администратора для очистки задолженности у выбранных экземпляров NetworkEntity.
        Args:
            request (HttpRequest): Объект HTTP-запроса.
            queryset (QuerySet): Набор выбранных объектов.
        """
        queryset.update(debt=0)
