from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count, Q

from users.decorators import teacher_required
from lms.models import Course, Lesson, Subscription
from users.models import User, LessonProgress, CourseProgress


@teacher_required
def teacher_dashboard(request):
    """Главная страница кабинета учителя"""
    teacher = request.user

    courses = Course.objects.filter(owner=teacher)

    courses_data = []
    for course in courses:
        # ✅ related_name='subscribers' у Subscription.course
        students_count = course.subscribers.count()
        lessons_count = course.lessons.count()

        courses_data.append({
            'course': course,
            'students_count': students_count,
            'lessons_count': lessons_count,
        })

    context = {
        'courses_data': courses_data,
        'total_courses': len(courses_data),
    }
    return render(request, 'lms/teacher/dashboard.html', context)


@teacher_required
def teacher_course_detail(request, course_id):
    """Детальная страница курса для учителя"""
    teacher = request.user
    course = get_object_or_404(Course, id=course_id, owner=teacher)

    lessons = course.lessons.all()   # ✅ related_name='lessons'

    # Ученики курса
    students = User.objects.filter(
        subscriptions__course=course
    ).annotate(
        completed_lessons=Count(
            'progress',
            filter=Q(progress__lesson__course=course, progress__is_completed=True)
        )
    )

    context = {
        'course': course,
        'lessons': lessons,
        'students': students,
    }
    return render(request, 'lms/teacher/course_detail.html', context)


@teacher_required
def teacher_students_list(request):
    """Список учеников"""
    teacher = request.user

    students = User.objects.filter(
        subscriptions__course__owner=teacher,
        is_student=True
    ).distinct().annotate(
        courses_count=Count('subscriptions', distinct=True)
    )

    context = {'students': students}
    return render(request, 'lms/teacher/students.html', context)


@teacher_required
def teacher_create_course(request):
    """Создание курса"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        if name:
            course = Course.objects.create(
                name=name,
                description=description,
                owner=request.user
            )
            messages.success(request, f'Курс "{course.name}" создан')
            return redirect('lms:teacher_course_detail', course_id=course.id)

    return render(request, 'lms/teacher/create_course.html')


@teacher_required
def teacher_create_lesson(request, course_id):
    """Создание урока"""
    course = get_object_or_404(Course, id=course_id, owner=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        video_url = request.POST.get('video_url')

        if name:
            lesson = Lesson.objects.create(
                name=name,
                description=description,
                video_url=video_url,
                course=course,
                owner=request.user
            )
            messages.success(request, f'Урок "{lesson.name}" создан')
            return redirect('lms:teacher_course_detail', course_id=course.id)

    return render(request, 'lms/teacher/create_lesson.html', {'course': course})


# ===== HTMX эндпоинты =====

@teacher_required
def teacher_lesson_edit_form(request, lesson_id):
    """Форма редактирования урока (HTMX)"""
    lesson = get_object_or_404(Lesson, id=lesson_id, owner=request.user)
    return render(request, 'lms/teacher/partials/lesson_edit_form.html', {
        'lesson': lesson,
    })


@teacher_required
def teacher_lesson_update(request, lesson_id):
    """Обновление урока (HTMX)"""
    if request.method != 'POST':
        return HttpResponse(status=405)

    lesson = get_object_or_404(Lesson, id=lesson_id, owner=request.user)

    lesson.name = request.POST.get('name', lesson.name)
    lesson.description = request.POST.get('description', lesson.description)
    lesson.video_url = request.POST.get('video_url', lesson.video_url)
    lesson.save()

    return render(request, 'lms/teacher/partials/lesson_row.html', {
        'lesson': lesson,
    })


@teacher_required
def teacher_lesson_delete(request, lesson_id):
    """Удаление урока (HTMX)"""
    if request.method != 'DELETE':
        return HttpResponse(status=405)

    lesson = get_object_or_404(Lesson, id=lesson_id, owner=request.user)
    lesson.delete()

    return HttpResponse('')
