from django.urls import path
from users.views import PaymentListAPIView, UserProfileView

urlpatterns = [
    # Список платежей с фильтрацией
    path('payments/', PaymentListAPIView.as_view(), name='payment-list'),

    # Профиль пользователя с историей платежей (* Дополнительное задание)
    path('users/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
]