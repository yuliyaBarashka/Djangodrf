from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=35, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
        ('card', 'Банковская карта'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'В ожидании'),
        ('paid', 'Оплачено'),
        ('failed', 'Ошибка'),
        ('canceled', 'Отменено'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey('lms.Course', on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    lesson = models.ForeignKey('lms.Lesson', on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='cash')

    # Поля для Stripe
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID сессии в Stripe')
    stripe_payment_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на оплату в Stripe')
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID цены в Stripe')
    stripe_product_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID продукта в Stripe')

    def __str__(self):
        return f"Payment {self.user.email} - {self.amount}"

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']