from django.db import models
from django.conf import settings


class Course(models.Model):
    """
    Модель курса.

    Поля:
        name: Название курса
        preview: Превью (картинка)
        description: Описание курса
        owner: Владелец курса
        stripe_product_id: ID продукта в Stripe
        updated_at: Дата последнего обновления (для Celery задач)
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    preview = models.ImageField(
        upload_to='courses/previews/',
        blank=True,
        null=True,
        verbose_name='Превью'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_courses',
        verbose_name='Владелец'
    )
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='ID продукта в Stripe'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-updated_at']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    Модель урока.

    Поля:
        name: Название урока
        description: Описание урока
        preview: Превью (картинка)
        video_url: Ссылка на видео (только YouTube)
        course: Связь с курсом
        owner: Владелец урока
        updated_at: Дата последнего обновления
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    preview = models.ImageField(
        upload_to='lessons/previews/',
        blank=True,
        null=True,
        verbose_name='Превью'
    )
    video_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='Ссылка на видео'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_lessons',
        verbose_name='Владелец'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['-updated_at']

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """
    Модель подписки на обновления курса.

    Поля:
        user: Пользователь, который подписался
        course: Курс, на который подписались
        created_at: Дата создания подписки
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Курс'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата подписки'
    )

    class Meta:
        # Уникальность пары пользователь-курс
        unique_together = ('user', 'course')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} -> {self.course.name}"