from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def manager_required(view_func):
    """Доступ только для сотрудников (Managers) и суперпользователей"""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('dashboard:login')

        is_manager = request.user.groups.filter(name='Managers').exists()
        is_superuser = request.user.is_superuser

        if not (is_manager or is_superuser):
            messages.error(request, 'Доступ запрещён. Только для сотрудников.')
            return redirect('dashboard:login')

        return view_func(request, *args, **kwargs)

    return wrapper
