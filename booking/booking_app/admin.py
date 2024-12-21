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

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'organizer', 'location', 'price', 'image')  # Поля для отображения
    search_fields = ('title', 'description', 'organizer__email')  # Поля для поиска
    list_filter = ('date', 'location')  # Фильтры
    ordering = ('date',)  # Сортировка
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'date', 'organizer', 'location', 'price', 'registered_users', 'image')
        }),
    )
    filter_horizontal = ('registered_users',)  # Удобный выбор для ManyToMany поля

#admin.site.register(Event, EventAdmin)


# Регистрируем модели
admin.site.register(User, UserAdmin)
#admin.site.register(Event)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(Event, EventAdmin)