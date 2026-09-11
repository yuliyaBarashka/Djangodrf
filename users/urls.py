from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import (
    UserRegistrationView, UserProfileView, UserListView,
    CustomTokenObtainPairView, PaymentListAPIView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('payments/', PaymentListAPIView.as_view(), name='payment_list'),
]