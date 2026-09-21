from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from users.models import User, Payment
from users.serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserUpdateSerializer,
    PaymentSerializer,
    UserPublicProfileSerializer
)


# ============================================================
# HTML-авторизация (для кабинетов ученика/учителя)
# ============================================================


def login_view(request):
    """Вход для учеников и учителей"""
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('lms:teacher_dashboard')
        if request.user.is_student:
            return redirect('lms:student_dashboard')
        return redirect('/')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.is_teacher:
                return redirect('lms:teacher_dashboard')
            if user.is_student:
                return redirect('lms:student_dashboard')
            return redirect('/')
        else:
            messages.error(request, 'Неверный email или пароль')

    return render(request, 'users/login.html')


def logout_view(request):
    """Выход"""
    logout(request)
    return redirect('/')


# ============================================================
# API: Регистрация и профиль
# ============================================================

class UserRegistrationView(generics.CreateAPIView):
    """Регистрация пользователя (доступно без авторизации)"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
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
                return UserPublicProfileSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)


class UserListView(generics.ListAPIView):
    """Список пользователей (только для админов)"""
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# ============================================================
# API: JWT-токены
# ============================================================

class CustomTokenObtainPairView(TokenObtainPairView):
    """Кастомный эндпоинт для получения токенов"""
    permission_classes = [AllowAny]


# ============================================================
# API: Платежи
# ============================================================

class PaymentListAPIView(generics.ListAPIView):
    """Список платежей с фильтрацией и сортировкой"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']