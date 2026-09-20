from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Админка
    path('admin/', admin.site.urls),

    # Дашборд сотрудника
    path('dashboard/', include('dashboard.urls')),

    # HTML-авторизация (login/logout для кабинетов)
    path('', include('users.urls_auth')),

    # Кабинеты ученика и учителя
    path('', include('lms.urls_cabinet')),

    # Основные страницы (главная, контакты, privacy, consent)
    path('', include('core.urls')),

    # API
    path('api/', include('lms.urls')),
    path('api/', include('users.urls')),

    # Документация API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

# Медиа и статика в DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
