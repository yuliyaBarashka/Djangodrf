from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView  # <-- Обязательно!
from rest_framework.permissions import IsAuthenticated, AllowAny  # <-- Добавьте AllowAny
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from lms.models import Course, Lesson, Subscription
from lms.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from users.permissions import IsModerator, IsOwner, IsModeratorOrOwner
from lms.paginators import CoursePaginator, LessonPaginator
from lms.services import create_payment_with_stripe, retrieve_stripe_session
from users.models import Payment
from django.conf import settings


@extend_schema(tags=['Courses'])
class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления курсами.

    Предоставляет полный CRUD для курсов с разграничением прав доступа:
    - Просмотр: все авторизованные пользователи
    - Создание: только не-модераторы
    - Редактирование: модераторы или владельцы
    - Удаление: только владельцы
    """
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
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@extend_schema(tags=['Lessons'])
class LessonListAPIView(generics.ListAPIView):
    """Список всех уроков с пагинацией"""
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LessonPaginator

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


@extend_schema(tags=['Lessons'])
class LessonCreateAPIView(generics.CreateAPIView):
    """
    Создание нового урока.

    Доступно только для не-модераторов.
    Владелец назначается автоматически.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@extend_schema(tags=['Lessons'])
class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр одного урока"""
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Moderators').exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=user)


@extend_schema(tags=['Lessons'])
class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Обновление урока.

    Доступно для модераторов или владельцев.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsModerator | IsOwner]


@extend_schema(tags=['Lessons'])
class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Удаление урока.

    Доступно только для владельцев.
    Модераторы НЕ МОГУТ удалять уроки.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]


@extend_schema(tags=['Subscriptions'])
class SubscriptionView(APIView):
    """
    Управление подпиской на курс.

    POST запрос с course_id:
    - Если подписка существует - удаляет её
    - Если подписки нет - создаёт новую
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=OpenApiTypes.OBJECT,
        responses={200: OpenApiTypes.OBJECT},
        examples=[
            OpenApiExample(
                'Успешный ответ',
                value={
                    "message": "Подписка добавлена",
                    "action": "subscribed",
                    "course_id": 1,
                    "course_name": "Python для начинающих"
                }
            )
        ]
    )
    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response(
                {"error": "Необходимо указать course_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = get_object_or_404(Course, id=course_id)
        subscription = Subscription.objects.filter(user=user, course=course)

        if subscription.exists():
            subscription.delete()
            message = "Подписка удалена"
            action = "unsubscribed"
        else:
            Subscription.objects.create(user=user, course=course)
            message = "Подписка добавлена"
            action = "subscribed"

        return Response({
            "message": message,
            "action": action,
            "course_id": course.id,
            "course_name": course.name
        }, status=status.HTTP_200_OK)


@extend_schema(tags=['Payments'])
class PaymentCreateView(APIView):
    """
    Создание платежа через Stripe

    POST запрос с данными о курсе и сумме.
    Возвращает ссылку на оплату в Stripe.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'course_id': {'type': 'integer', 'description': 'ID курса'},
                    'amount': {'type': 'number', 'description': 'Сумма платежа в рублях'},
                },
                'required': ['course_id', 'amount']
            }
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'payment_id': {'type': 'integer'},
                    'amount': {'type': 'string'},
                    'payment_url': {'type': 'string'},
                    'session_id': {'type': 'string'},
                    'status': {'type': 'string'},
                }
            },
            400: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
            404: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        }
    )
    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        amount = request.data.get('amount')

        if not course_id or not amount:
            return Response(
                {"error": "Необходимо указать course_id и amount"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(
                {"error": "Курс не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Проверяем, что пользователь не оплачивает свой курс
        if course.owner == user:
            return Response(
                {"error": "Вы не можете оплатить свой собственный курс"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # URL для перенаправления после оплаты
        success_url = request.build_absolute_uri('/api/payments/success/')
        cancel_url = request.build_absolute_uri('/api/payments/cancel/')

        try:
            payment_data = create_payment_with_stripe(
                user=user,
                course=course,
                amount=float(amount),
                success_url=success_url,
                cancel_url=cancel_url
            )
            return Response(payment_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(tags=['Payments'])
class PaymentStatusView(APIView):
    """
    Получение статуса платежа из Stripe
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='payment_id',
                type=int,
                location=OpenApiParameter.QUERY,
                description='ID платежа в системе',
                required=True
            )
        ],
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'payment_status': {'type': 'string'},
                    'amount': {'type': 'string'},
                    'currency': {'type': 'string'},
                }
            },
            404: {'type': 'object', 'properties': {'error': {'type': 'string'}}},
        }
    )
    def get(self, request):
        payment_id = request.query_params.get('payment_id')

        if not payment_id:
            return Response(
                {"error": "Необходимо указать payment_id"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payment = Payment.objects.get(id=payment_id, user=request.user)
        except Payment.DoesNotExist:
            return Response(
                {"error": "Платеж не найден"},
                status=status.HTTP_404_NOT_FOUND
            )

        if not payment.stripe_session_id:
            return Response(
                {"error": "У этого платежа нет связанной сессии в Stripe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            session_data = retrieve_stripe_session(payment.stripe_session_id)

            # Обновляем статус платежа в БД
            if session_data['payment_status'] == 'paid':
                payment.status = 'paid'
                payment.save()

            return Response({
                'status': payment.status,
                'payment_status': session_data['payment_status'],
                'amount': session_data.get('amount_total', payment.amount),
                'currency': session_data.get('currency', 'rub'),
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


@extend_schema(tags=['Payments'])
class PaymentSuccessView(APIView):
    """
    Страница успешной оплаты (редирект после оплаты)
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "message": "Оплата прошла успешно! Спасибо за покупку.",
            "status": "success"
        })


@extend_schema(tags=['Payments'])
class PaymentCancelView(APIView):
    """
    Страница отмены оплаты
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "message": "Оплата была отменена. Попробуйте снова.",
            "status": "canceled"
        })