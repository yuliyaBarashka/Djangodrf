from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModerator, IsOwner, IsModeratorOrOwner
from lms.paginators import CoursePaginator, LessonPaginator


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, IsOwner]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Course.objects.all()
        return Course.objects.filter(owner=user)

    def get_serializer_context(self):
        """Передаем request в контекст для проверки подписки"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LessonPaginator  

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


# ===== УПРАВЛЕНИЕ ПОДПИСКОЙ =====
class SubscriptionView(APIView):
    """Эндпоинт для управления подпиской на курс"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "Необходимо указать course_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)

        # Проверяем, есть ли подписка
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            # Если есть - удаляем
            subscription.delete()
            message = "Подписка удалена"
            action = "unsubscribed"
        else:
            # Если нет - создаем
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"
            action = "subscribed"

        return Response({
            "message": message,
            "action": action,
            "course_id": course.id,
            "course_name": course.name
        }, status=status.HTTP_200_OK)