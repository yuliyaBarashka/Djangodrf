from django.urls import path
from dashboard import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('requests/', views.requests_list, name='requests'),
    path('requests/<int:pk>/', views.request_detail, name='request_detail'),
    path('requests/<int:pk>/processed/', views.request_mark_processed, name='request_mark_processed'),
    path('requests/<int:pk>/delete/', views.request_delete, name='request_delete'),
]
