from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Count, Q

from users.decorators import student_required
from lms.models import Course, Lesson, Subscription
from users.models import LessonProgress, CourseProgress


@student_required
def student_dashboard(request):
    """Главная страница кабинета ученика"""
    student = request.user

    # Курсы, на которые подписан
    subscriptions = Subscription.objects.filter(user=student).select_related('course')
    courses = [sub.course for sub in subscriptions]

    # Прогресс по курсам
    courses_data = []
    for course in courses:
        total_lessons = course.lessons.count()   # ✅ related_name='lessons'
        completed_lessons = LessonProgress.objects.filter(
            student=student,
            lesson__course=course,
            is_completed=True
        ).count()

        progress_percent = 0
        if total_lessons > 0:
            progress_percent = int((completed_lessons / total_lessons) * 100)

        courses_data.append({
            'course': course,
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'progress_percent': progress_percent,
        })

    context = {
        'courses_data': courses_data,
        'total_courses': len(courses_data),
    }
    return render(request, 'lms/student/dashboard.html', context)


@student_required
def student_course_detail(request, course_id):
    """Детальная страница курса для ученика"""
    student = request.user
    course = get_object_or_404(Course, id=course_id)

    is_subscribed = Subscription.objects.filter(user=student, course=course).exists()

    # Если в Lesson нет поля order — убираем .order_by('order')
    lessons = course.lessons.all()

    lessons_data = []
    for lesson in lessons:
        progress, _ = LessonProgress.objects.get_or_create(
            student=student,
            lesson=lesson
        )
        lessons_data.append({
            'lesson': lesson,
            'is_completed': progress.is_completed,
        })

    context = {
        'course': course,
        'lessons_data': lessons_data,
        'is_subscribed': is_subscribed,
    }
    return render(request, 'lms/student/course_detail.html', context)


@student_required
def student_lesson_detail(request, lesson_id):
    """Детальная страница урока"""
    student = request.user
    lesson = get_object_or_404(Lesson, id=lesson_id)

    progress, _ = LessonProgress.objects.get_or_create(
        student=student,
        lesson=lesson
    )

    context = {
        'lesson': lesson,
        'progress': progress,
    }
    return render(request, 'lms/student/lesson_detail.html', context)


@student_required
def mark_lesson_complete(request, lesson_id):
    """Отметить урок как пройденный (HTMX)"""
    if request.method != 'POST':
        return HttpResponse(status=405)

    student = request.user
    lesson = get_object_or_404(Lesson, id=lesson_id)

    progress, _ = LessonProgress.objects.get_or_create(
        student=student,
        lesson=lesson
    )
    progress.is_completed = True
    progress.completed_at = timezone.now()
    progress.save()

    return render(request, 'lms/student/partials/lesson_status.html', {
        'lesson': lesson,
        'progress': progress,
    })


@student_required
def student_profile(request):
    """Профиль ученика"""
    student = request.user

    total_completed = LessonProgress.objects.filter(
        student=student,
        is_completed=True
    ).count()

    context = {
        'total_completed': total_completed,
    }
    return render(request, 'lms/student/profile.html', context)
