from django.db import models
from django.conf import settings


class Course(models.Model):
    name = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='courses/previews/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_courses'
    )

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    preview = models.ImageField(upload_to='lessons/previews/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_lessons'
    )

    def __str__(self):
        return self.name


class Subscription(models.Model):
    """Модель подписки на обновления курса"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Уникальность пары пользователь-курс
        unique_together = ('user', 'course')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f"{self.user.email} -> {self.course.name}"
    