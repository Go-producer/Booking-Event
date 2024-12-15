from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Event, Role, UserRole

# Класс для отображения пользователя в админке
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'is_active', 'is_staff', 'is_admin')  # Поля для отображения
    search_fields = ('email', 'name')  # Поля для поиска
    readonly_fields = ('id', 'last_login')  # Поля, которые нельзя редактировать

    filter_horizontal = ('groups', 'user_permissions')
    list_filter = ('is_staff', 'is_active', 'is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

    ordering = ('email',)

# Регистрируем модели
admin.site.register(User, UserAdmin)
admin.site.register(Event)
admin.site.register(Role)
admin.site.register(UserRole)
