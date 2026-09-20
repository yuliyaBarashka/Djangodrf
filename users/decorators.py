from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def student_required(view_func):
    """Доступ только для учеников"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not request.user.is_student:
            messages.error(request, 'Доступ только для учеников')
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper


def teacher_required(view_func):
    """Доступ только для учителей"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:login')
        if not request.user.is_teacher:
            messages.error(request, 'Доступ только для учителей')
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return wrapper
