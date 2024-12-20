from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings

# Менеджер пользователя
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('Пользователи должны иметь адрес электронной почты')
        if self.model.objects.filter(email=email).exists():
            raise ValueError('Пользователь с таким email уже существует')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

# Модель пользователя
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)  # Уникальность email
    name = models.CharField(max_length=40, unique=True)  # Логин (если нужен уникальный)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)  # Новый флаг администратора

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Уникальное имя для избежания конфликта
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Уникальное имя для избежания конфликта
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Email используется для входа
    REQUIRED_FIELDS = ['name']  # Обязательное поле при создании суперпользователя

    def __str__(self):
        return self.email

    @property
    def is_superuser(self):
        return self.is_admin



# Модель ролей
class Role(models.Model):
    code = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=40, unique=True)

    def __str__(self):
        return self.name

# Роли пользователей
class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'role')

# Модель мероприятий

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    registered_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,  # Указывает на вашу кастомную модель User
        related_name='registered_events',  # Связь для обратного вызова
        blank=True
    )

    def __str__(self):
        return self.title
