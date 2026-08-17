from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User, Payment
from users.serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    PaymentSerializer,
    UserPublicProfileSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    """Регистрация пользователя (доступно без авторизации)"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):  # ✅ Добавлен Destroy
    """
    Просмотр, редактирование и удаление профиля пользователя
    - Просмотр любого профиля (с ограничением данных для чужих)
    - Редактирование и удаление только своего профиля
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        """Разные сериализаторы для разных методов"""
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserProfileSerializer

    def get_object(self):
        """Проверка прав на доступ к объекту"""
        obj = super().get_object()

        # Для методов изменения и удаления проверяем, что это свой профиль
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.pk != self.request.user.pk:
                self.permission_denied(
                    self.request,
                    message="Вы можете изменять или удалять только свой профиль"
                )
        return obj

    def get_serializer(self, *args, **kwargs):
        """Для просмотра чужого профиля показываем только публичную информацию"""
        if self.request.method == 'GET':
            obj = self.get_object()
            if obj.pk != self.request.user.pk:
                # Если смотрим чужой профиль - используем публичный сериализатор
                return UserPublicProfileSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)


class UserListView(generics.ListAPIView):
    """Список пользователей (только для админов)"""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class CustomTokenObtainPairView(TokenObtainPairView):
    """Кастомный эндпоинт для получения токенов"""
    permission_classes = [AllowAny]


class PaymentListAPIView(generics.ListAPIView):
    """Список платежей с фильтрацией и сортировкой"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']