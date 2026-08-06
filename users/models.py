from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Отключаем поле username, делаем email обязательным и уникальным
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')

    # Добавляем новые поля
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Аватарка')

    # Указываем, что для входа используется email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Убираем username из обязательных полей

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        