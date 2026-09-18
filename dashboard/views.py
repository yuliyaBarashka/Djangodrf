from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Q

from core.models import ContactRequest
from users.models import User
from .decorators import manager_required


def login_view(request):
    """Страница входа для сотрудников"""
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)

        if user is not None:
            is_manager = user.groups.filter(name='Managers').exists()
            if user.is_superuser or is_manager:
                login(request, user)
                return redirect('dashboard:index')
            else:
                messages.error(request, 'Доступ запрещён. Вы не сотрудник.')
        else:
            messages.error(request, 'Неверный email или пароль')

    return render(request, 'dashboard/login.html')


def logout_view(request):
    """Выход"""
    logout(request)
    return redirect('dashboard:login')


@manager_required
def index(request):
    """Главная страница дашборда"""

    # Статистика
    total_requests = ContactRequest.objects.count()
    unprocessed = ContactRequest.objects.filter(is_processed=False).count()
    processed = ContactRequest.objects.filter(is_processed=True).count()

    # За сегодня
    today = timezone.now().date()
    today_requests = ContactRequest.objects.filter(
        created_at__date=today
    ).count()

    # За последние 7 дней
    week_ago = timezone.now() - timedelta(days=7)
    week_requests = ContactRequest.objects.filter(
        created_at__gte=week_ago
    ).count()

    # Последние 10 заявок
    latest_requests = ContactRequest.objects.all()[:10]

    # Статистика по дням (для графика)
    days_stats = []
    for i in range(6, -1, -1):
        day = timezone.now().date() - timedelta(days=i)
        count = ContactRequest.objects.filter(created_at__date=day).count()
        days_stats.append({
            'date': day.strftime('%d.%m'),
            'count': count,
        })

    context = {
        'total_requests': total_requests,
        'unprocessed': unprocessed,
        'processed': processed,
        'today_requests': today_requests,
        'week_requests': week_requests,
        'latest_requests': latest_requests,
        'days_stats': days_stats,
        'user': request.user,
    }

    return render(request, 'dashboard/index.html', context)


@manager_required
def requests_list(request):
    """Список всех заявок"""
    requests = ContactRequest.objects.all()

    # Фильтры
    status_filter = request.GET.get('status', 'all')
    if status_filter == 'unprocessed':
        requests = requests.filter(is_processed=False)
    elif status_filter == 'processed':
        requests = requests.filter(is_processed=True)

    # Поиск
    search = request.GET.get('search', '')
    if search:
        requests = requests.filter(
            Q(name__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search) |
            Q(message__icontains=search)
        )

    context = {
        'requests': requests,
        'status_filter': status_filter,
        'search': search,
        'user': request.user,
    }

    return render(request, 'dashboard/requests.html', context)


@manager_required
def request_detail(request, pk):
    """Просмотр одной заявки"""
    contact = get_object_or_404(ContactRequest, pk=pk)

    if request.method == 'POST':
        contact.is_processed = True
        contact.save()
        messages.success(request, 'Заявка отмечена как обработанная')
        return redirect('dashboard:requests')

    context = {
        'contact': contact,
        'user': request.user,
    }

    return render(request, 'dashboard/request_detail.html', context)


@manager_required
def request_mark_processed(request, pk):
    """Отметить как обработанную"""
    contact = get_object_or_404(ContactRequest, pk=pk)
    contact.is_processed = True
    contact.save()
    messages.success(request, 'Заявка обработана')
    return redirect('dashboard:requests')


@manager_required
def request_delete(request, pk):
    """Удалить заявку (только суперпользователь)"""
    if not request.user.is_superuser:
        messages.error(request, 'Только суперпользователь может удалять')
        return redirect('dashboard:requests')

    contact = get_object_or_404(ContactRequest, pk=pk)
    contact.delete()
    messages.success(request, 'Заявка удалена')
    return redirect('dashboard:requests')
