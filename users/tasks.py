from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def block_inactive_users():
    """
    Задача для блокировки пользователей, которые не заходили более месяца.
    Запускается ежедневно по расписанию (Celery Beat).
    """
    # Вычисляем дату месяц назад
    one_month_ago = timezone.now() - timedelta(days=30)

    # Находим пользователей, которые не заходили более месяца и еще активны
    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True,
        is_superuser=False  # Не блокируем суперпользователей
    )

    count = inactive_users.count()

    if count == 0:
        return f"No inactive users found. (Last month: {one_month_ago})"

    # Блокируем пользователей (обновляем батчем)
    inactive_users.update(is_active=False)

    return f"Blocked {count} inactive users (last login before {one_month_ago})"
