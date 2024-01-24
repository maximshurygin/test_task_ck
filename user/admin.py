from django.contrib import admin

from user.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Класс администратора для модели User.

    Определяет, как пользовательские объекты отображаются и управляются в административной панели Django.

    Атрибуты:
        list_display (tuple): Поля, которые будут отображаться в списке пользователей на админ-панели.
    """
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_active')
