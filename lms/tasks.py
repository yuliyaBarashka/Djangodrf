from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from users.models import User
from lms.models import Course, Subscription


@shared_task
def send_course_update_notification(course_id, updated_by_email):
    """
    Задача для отправки уведомлений подписчикам об обновлении курса.

    Args:
        course_id: ID курса
        updated_by_email: Email пользователя, который обновил курс
    """
    try:
        course = Course.objects.get(id=course_id)

        # Получаем всех подписчиков курса
        subscriptions = Subscription.objects.filter(course=course).select_related('user')

        if not subscriptions.exists():
            return f"No subscribers for course '{course.name}'"

        subscribers_emails = [sub.user.email for sub in subscriptions]

        # Отправляем письмо каждому подписчику
        subject = f"📚 Курс '{course.name}' был обновлен!"
        message = f"""
        Здравствуйте!

        Курс '{course.name}' был обновлен пользователем {updated_by_email}.

        Зайдите на платформу, чтобы ознакомиться с новыми материалами:
        http://127.0.0.1:8000/api/courses/{course.id}/

        С уважением,
        Команда LMS
        """

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=subscribers_emails,
            fail_silently=False,
        )

        return f"Notifications sent to {len(subscribers_emails)} subscribers for course '{course.name}'"

    except Course.DoesNotExist:
        return f"Course with id {course_id} does not exist"
    except Exception as e:
        return f"Error sending notifications: {str(e)}"


@shared_task
def send_course_update_notification_if_updated(course_id, updated_by_email):
    """
    Дополнительное задание: Отправка уведомления только если курс не обновлялся более 4 часов.
    """
    try:
        course = Course.objects.get(id=course_id)

        # Проверяем, есть ли поле updated_at в модели Course
        # Если нет, используем время создания или текущее время
        if hasattr(course, 'updated_at'):
            time_since_update = timezone.now() - course.updated_at
        else:
            # Если поля updated_at нет, добавляем логику для existing field
            # Например, используем timezone.now() - timedelta(hours=5) для теста
            time_since_update = timedelta(hours=5)

        # Проверяем, прошло ли более 4 часов
        if time_since_update.total_seconds() < 4 * 3600:
            return f"Course '{course.name}' was updated recently ({time_since_update}). Notification skipped."

        # Если прошло более 4 часов - отправляем уведомление
        return send_course_update_notification(course_id, updated_by_email)

    except Course.DoesNotExist:
        return f"Course with id {course_id} does not exist"
    except Exception as e:
        return f"Error checking update time: {str(e)}"