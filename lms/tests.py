from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import Group
from users.models import User
from lms.models import Course, Lesson, Subscription


class LessonAPITestCase(TestCase):
    """Тесты для CRUD уроков"""

    def setUp(self):
        """Подготовка данных для тестов"""
        # Создаем клиента
        self.client = APIClient()

        # Создаем пользователей
        self.user = User.objects.create(
            email='user@test.com',
            first_name='Test',
            last_name='User'
        )
        self.user.set_password('testpass123')
        self.user.save()

        self.moderator = User.objects.create(
            email='moderator@test.com',
            first_name='Moderator',
            last_name='Test'
        )
        self.moderator.set_password('testpass123')
        self.moderator.save()

        # Добавляем модератора в группу
        moderator_group, _ = Group.objects.get_or_create(name='Moderators')
        self.moderator.groups.add(moderator_group)

        # Создаем курс
        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            owner=self.user
        )

        # Данные для создания урока
        self.lesson_data = {
            'name': 'Test Lesson',
            'description': 'Test Lesson Description',
            'video_url': 'https://www.youtube.com/watch?v=test',
            'course': self.course.id
        }

        self.lesson_data_invalid_url = {
            'name': 'Test Lesson',
            'description': 'Test Lesson Description',
            'video_url': 'https://vk.com/video/test',
            'course': self.course.id
        }

    def test_create_lesson_authenticated(self):
        """Тест создания урока авторизованным пользователем"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('lesson_create'),
            self.lesson_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(Lesson.objects.first().owner, self.user)

    def test_create_lesson_unauthenticated(self):
        """Тест создания урока неавторизованным пользователем"""
        response = self.client.post(
            reverse('lesson_create'),
            self.lesson_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_lesson_moderator(self):
        """Тест создания урока модератором (должен быть запрет)"""
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(
            reverse('lesson_create'),
            self.lesson_data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_lesson_invalid_url(self):
        """Тест создания урока с недопустимой ссылкой"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('lesson_create'),
            self.lesson_data_invalid_url,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Разрешены только ссылки на YouTube', str(response.data))

    def test_list_lessons(self):
        """Тест получения списка уроков"""
        # Создаем урок
        lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Test Description',
            video_url='https://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('lesson_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # С пагинацией

    def test_update_lesson_owner(self):
        """Тест обновления урока владельцем"""
        lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Test Description',
            video_url='https://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse('lesson_update', args=[lesson.id]),
            {'name': 'Updated Lesson'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Lesson')

    def test_update_lesson_moderator(self):
        """Тест обновления урока модератором (разрешено)"""
        lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Test Description',
            video_url='https://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )

        self.client.force_authenticate(user=self.moderator)
        response = self.client.patch(
            reverse('lesson_update', args=[lesson.id]),
            {'name': 'Updated by Moderator'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated by Moderator')

    def test_update_lesson_other_user(self):
        """Тест обновления урока другим пользователем (запрещено)"""
        other_user = User.objects.create(
            email='other@test.com',
            first_name='Other',
            last_name='User'
        )
        other_user.set_password('testpass123')
        other_user.save()

        lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Test Description',
            video_url='https://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )

        self.client.force_authenticate(user=other_user)
        response = self.client.patch(
            reverse('lesson_update', args=[lesson.id]),
            {'name': 'Updated by Other'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_lesson_owner(self):
        """Тест удаления урока владельцем"""
        lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Test Description',
            video_url='https://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse('lesson_delete', args=[lesson.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_delete_lesson_moderator(self):
        """Тест удаления урока модератором (запрещено)"""
        lesson = Lesson.objects.create(
            name='Test Lesson',
            description='Test Description',
            video_url='https://www.youtube.com/watch?v=test',
            course=self.course,
            owner=self.user
        )

        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(
            reverse('lesson_delete', args=[lesson.id])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SubscriptionAPITestCase(TestCase):
    """Тесты для подписки"""

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create(
            email='user@test.com',
            first_name='Test',
            last_name='User'
        )
        self.user.set_password('testpass123')
        self.user.save()

        self.course = Course.objects.create(
            name='Test Course',
            description='Test Description',
            owner=self.user
        )

    def test_subscribe_to_course(self):
        """Тест подписки на курс"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('subscriptions'),
            {'course_id': self.course.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'subscribed')
        self.assertEqual(Subscription.objects.count(), 1)

    def test_unsubscribe_from_course(self):
        """Тест отписки от курса"""
        # Создаем подписку
        Subscription.objects.create(
            user=self.user,
            course=self.course
        )

        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('subscriptions'),
            {'course_id': self.course.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['action'], 'unsubscribed')
        self.assertEqual(Subscription.objects.count(), 0)

    def test_subscription_without_course_id(self):
        """Тест подписки без указания course_id"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('subscriptions'),
            {},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('course_id', str(response.data))

    def test_subscription_invalid_course(self):
        """Тест подписки на несуществующий курс"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse('subscriptions'),
            {'course_id': 999},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscription_unauthenticated(self):
        """Тест подписки без авторизации"""
        response = self.client.post(
            reverse('subscriptions'),
            {'course_id': self.course.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)