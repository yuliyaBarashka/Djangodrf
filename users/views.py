from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import User, Payment
from users.serializers import (
    UserRegistrationSerializer, UserProfileSerializer,
    UserUpdateSerializer, PaymentSerializer, UserPublicProfileSerializer
)


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserProfileSerializer

    def get_object(self):
        obj = super().get_object()
        if self.request.method in ['PUT', 'PATCH'] and obj.pk != self.request.user.pk:
            self.permission_denied(self.request, message="Вы можете редактировать только свой профиль")
        return obj

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET' and self.get_object().pk != self.request.user.pk:
            return UserPublicProfileSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']
    