from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages

from users.decorators import student_required
from lms.models import (
    Course, Lesson, Subscription, Submission,
    TestQuestion, StudentAnswer,
)
from users.models import LessonProgress


# ============================================================
# ПУБЛИЧНАЯ СТРАНИЦА КУРСА
# ============================================================

def course_preview(request, course_id):
    """Публичная страница курса ДО покупки."""
    course = get_object_or_404(Course, id=course_id)
    lessons = course.lessons.all().order_by('order', 'id')

    is_subscribed = False
    if request.user.is_authenticated:
        is_subscribed = Subscription.objects.filter(
            user=request.user, course=course
        ).exists()

    return render(request, 'lms/student/course_preview.html', {
        'course': course,
        'lessons': lessons,
        'is_subscribed': is_subscribed,
    })


# ============================================================
# КАБИНЕТ УЧЕНИКА
# ============================================================

@student_required
def student_dashboard(request):
    """Главная страница кабинета ученика."""
    student = request.user

    subscriptions = Subscription.objects.filter(user=student).select_related('course')
    courses = [sub.course for sub in subscriptions]

    courses_data = []
    for course in courses:
        total_lessons = course.lessons.count()
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

    return render(request, 'lms/student/dashboard.html', {
        'courses_data': courses_data,
        'total_courses': len(courses_data),
    })


@student_required
def student_course_detail(request, course_id):
    """Детальная страница курса для ученика."""
    student = request.user
    course = get_object_or_404(Course, id=course_id)

    is_subscribed = Subscription.objects.filter(user=student, course=course).exists()

    lessons = course.lessons.all().order_by('order', 'id')

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

    return render(request, 'lms/student/course_detail.html', {
        'course': course,
        'lessons_data': lessons_data,
        'is_subscribed': is_subscribed,
    })


@student_required
def student_lesson_detail(request, lesson_id):
    """Детальная страница урока."""
    student = request.user
    lesson = get_object_or_404(Lesson, id=lesson_id)

    progress, _ = LessonProgress.objects.get_or_create(
        student=student,
        lesson=lesson
    )

    submission = None
    if lesson.is_test:
        submission = Submission.objects.filter(
            student=student, lesson=lesson
        ).first()

    return render(request, 'lms/student/lesson_detail.html', {
        'lesson': lesson,
        'progress': progress,
        'submission': submission,
    })


@student_required
def mark_lesson_complete(request, lesson_id):
    """Отметить урок как пройденный (HTMX)."""
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
    """Профиль ученика."""
    student = request.user

    total_completed = LessonProgress.objects.filter(
        student=student,
        is_completed=True
    ).count()

    return render(request, 'lms/student/profile.html', {
        'total_completed': total_completed,
    })


# ============================================================
# РАБОЧАЯ ТЕТРАДЬ — загрузка PDF
# ============================================================

@student_required
def student_submit_workbook(request, lesson_id):
    """Ученик загружает заполненную рабочую тетрадь."""
    if request.method != 'POST':
        return HttpResponse(status=405)

    student = request.user
    lesson = get_object_or_404(Lesson, id=lesson_id)

    file = request.FILES.get('file')
    if not file:
        messages.error(request, 'Нужно прикрепить файл')
        return redirect('lms:student_lesson_detail', lesson_id=lesson.id)

    Submission.objects.update_or_create(
        student=student,
        lesson=lesson,
        defaults={
            'file': file,
            'status': 'submitted',
            'submitted_at': timezone.now(),
            'score': None,
            'teacher_comment': '',
        }
    )

    messages.success(request, 'Работа отправлена на проверку')
    return redirect('lms:student_lesson_detail', lesson_id=lesson.id)


# ============================================================
# КОНТРОЛЬНАЯ — онлайн-тест
# ============================================================

@student_required
def student_test_start(request, lesson_id):
    """Страница прохождения контрольной."""
    student = request.user
    lesson = get_object_or_404(Lesson, id=lesson_id, is_test=True)

    submission = Submission.objects.filter(student=student, lesson=lesson).first()

    if submission and submission.status in ('submitted', 'checked'):
        return render(request, 'lms/student/test_result.html', {
            'lesson': lesson,
            'submission': submission,
        })

    questions = lesson.questions.prefetch_related('answers').all()

    return render(request, 'lms/student/test_form.html', {
        'lesson': lesson,
        'questions': questions,
        'submission': submission,
    })


@student_required
def student_test_submit(request, lesson_id):
    """Приём ответов на контрольную."""
    if request.method != 'POST':
        return HttpResponse(status=405)

    student = request.user
    lesson = get_object_or_404(Lesson, id=lesson_id, is_test=True)
    questions = lesson.questions.all()

    submission, _ = Submission.objects.update_or_create(
        student=student,
        lesson=lesson,
        defaults={
            'status': 'submitted',
            'submitted_at': timezone.now(),
            'score': None,
            'teacher_comment': '',
        }
    )

    for question in questions:
        StudentAnswer.objects.filter(submission=submission, question=question).delete()
        sa = StudentAnswer(submission=submission, question=question)

        if question.question_type == 'single':
            answer_id = request.POST.get(f'question_{question.id}')
            sa.save()
            if answer_id:
                sa.selected_answers.set([answer_id])

        elif question.question_type == 'multiple':
            answer_ids = request.POST.getlist(f'question_{question.id}')
            sa.save()
            if answer_ids:
                sa.selected_answers.set(answer_ids)

        elif question.question_type == 'text':
            sa.text_answer = request.POST.get(f'question_{question.id}', '')
            sa.save()

        elif question.question_type == 'file':
            file = request.FILES.get(f'question_{question.id}')
            if file:
                sa.file_answer = file
            sa.save()

    messages.success(request, 'Работа отправлена на проверку')
    return redirect('lms:student_lesson_detail', lesson_id=lesson.id)