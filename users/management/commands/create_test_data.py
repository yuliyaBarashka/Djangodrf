from django.core.management.base import BaseCommand
from users.models import User, Payment
from lms.models import Course, Lesson
from django.utils import timezone


class Command(BaseCommand):
    help = 'Создает тестовые данные для платежей'

    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных...')

        # Создаем пользователя
        user, created = User.objects.get_or_create(
            email='test@example.com',
            defaults={
                'first_name': 'Тест',
                'last_name': 'Пользователь'
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(f'Создан пользователь: {user.email}')

        # Создаем курс
        course, created = Course.objects.get_or_create(
            name='Python для начинающих',
            defaults={
                'description': 'Полный курс по Python с нуля'
            }
        )
        if created:
            self.stdout.write(f'Создан курс: {course.name}')

        # Создаем уроки
        lesson1, created = Lesson.objects.get_or_create(
            name='Введение в Python',
            defaults={
                'description': 'Установка и первые шаги',
                'course': course
            }
        )
        if created:
            self.stdout.write(f'Создан урок: {lesson1.name}')

        lesson2, created = Lesson.objects.get_or_create(
            name='Переменные и типы данных',
            defaults={
                'description': 'Основы Python',
                'course': course
            }
        )
        if created:
            self.stdout.write(f'Создан урок: {lesson2.name}')

        # Создаем платежи
        payment1, created = Payment.objects.get_or_create(
            user=user,
            course=course,
            defaults={
                'amount': 5000.00,
                'payment_method': 'transfer'
            }
        )
        if created:
            self.stdout.write('Создан платеж на курс')

        payment2, created = Payment.objects.get_or_create(
            user=user,
            lesson=lesson1,
            defaults={
                'amount': 1000.00,
                'payment_method': 'cash'
            }
        )
        if created:
            self.stdout.write('Создан платеж на урок')

        self.stdout.write(self.style.SUCCESS('Тестовые данные созданы!'))
        