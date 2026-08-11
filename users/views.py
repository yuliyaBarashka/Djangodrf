from rest_framework import generics, viewsets
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from users.models import User, Payment
from users.serializers import PaymentSerializer, UserProfileSerializer


class PaymentListAPIView(generics.ListAPIView):
    """Список платежей с фильтрацией и сортировкой"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # Настройка фильтрации и сортировки
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # Поля для фильтрации
    filterset_fields = {
        'course': ['exact'],  # Фильтр по ID курса
        'lesson': ['exact'],  # Фильтр по ID урока
        'payment_method': ['exact'],  # Фильтр по способу оплаты
    }

    # Поля для сортировки
    ordering_fields = ['payment_date']
    ordering = ['-payment_date']  # По умолчанию - новые сверху


# * Дополнительное задание: просмотр профиля с историей платежей
class UserProfileView(generics.RetrieveAPIView):
    """Просмотр профиля пользователя с историей платежей"""

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'
    