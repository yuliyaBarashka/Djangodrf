from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone

from users.decorators import teacher_required
from lms.models import (
    Course, Lesson, Submission, Subscription,
    TestQuestion, TestAnswer,
)
from users.models import User, LessonProgress


# ============================================================
# ДАШБОРД
# ============================================================

@teacher_required
def teacher_dashboard(request):
    """Главная страница кабинета учителя."""
    teacher = request.user
    courses = Course.objects.filter(owner=teacher)

    courses_data = []
    for course in courses:
        courses_data.append({
            'course': course,
            'students_count': course.subscribers.count(),
            'lessons_count': course.lessons.count(),
        })

    pending_submissions = Submission.objects.filter(
        lesson__course__owner=teacher,
        status='submitted',
    ).count()

    return render(request, 'lms/teacher/dashboard.html', {
        'courses_data': courses_data,
        'total_courses': len(courses_data),
        'pending_submissions': pending_submissions,
    })


@teacher_required
def teacher_course_detail(request, course_id):
    """Детальная страница курса для учителя."""
    teacher = request.user
    course = get_object_or_404(Course, id=course_id, owner=teacher)

    lessons = course.lessons.all().order_by('order', 'id')

    students = User.objects.filter(
        subscriptions__course=course
    ).annotate(
        completed_lessons=Count(
            'progress',
            filter=Q(progress__lesson__course=course, progress__is_completed=True)
        )
    )

    return render(request, 'lms/teacher/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'students': students,
    })


@teacher_required
def teacher_students_list(request):
    """Список учеников учителя."""
    teacher = request.user

    students = User.objects.filter(
        subscriptions__course__owner=teacher,
        is_student=True
    ).distinct().annotate(
        courses_count=Count('subscriptions', distinct=True)
    )

    return render(request, 'lms/teacher/students.html', {'students': students})


# ============================================================
# СОЗДАНИЕ КУРСА
# ============================================================

@teacher_required
def teacher_create_course(request):
    """Создание курса."""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price', '0')
        is_published = request.POST.get('is_published') == 'on'

        if name:
            course = Course.objects.create(
                name=name,
                description=description,
                price=price or 0,
                is_published=is_published,
                owner=request.user,
            )
            messages.success(request, f'Курс "{course.name}" создан')
            return redirect('lms:teacher_course_detail', course_id=course.id)

    return render(request, 'lms/teacher/create_course.html')


# ============================================================
# СОЗДАНИЕ УРОКА
# ============================================================

@teacher_required
def teacher_create_lesson(request, course_id):
    """Создание урока с файлами."""
    course = get_object_or_404(Course, id=course_id, owner=request.user)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        video_url = request.POST.get('video_url') or None
        order = int(request.POST.get('order', 0) or 0)
        is_test = request.POST.get('is_test') == 'on'
        max_score = int(request.POST.get('max_score', 100) or 100)

        if name:
            lesson = Lesson.objects.create(
                name=name,
                description=description,
                video_url=video_url,
                order=order,
                is_test=is_test,
                max_score=max_score,
                lecture_pdf=request.FILES.get('lecture_pdf'),
                workbook_pdf=request.FILES.get('workbook_pdf'),
                test_file=request.FILES.get('test_file'),
                course=course,
                owner=request.user,
            )
            messages.success(request, f'Урок "{lesson.name}" создан')

            if is_test:
                return redirect('lms:teacher_test_questions', lesson_id=lesson.id)
            return redirect('lms:teacher_course_detail', course_id=course.id)

    return render(request, 'lms/teacher/create_lesson.html', {'course': course})


# ============================================================
# HTMX — РЕДАКТИРОВАНИЕ УРОКА
# ============================================================

@teacher_required
def teacher_lesson_edit_form(request, lesson_id):
    """Форма редактирования урока (HTMX)."""
    lesson = get_object_or_404(Lesson, id=lesson_id, owner=request.user)
    return render(request, 'lms/teacher/partials/lesson_edit_form.html', {
        'lesson': lesson,
    })


@teacher_required
def teacher_lesson_update(request, lesson_id):
    """Обновление урока (HTMX)."""
    if request.method != 'POST':
        return HttpResponse(status=405)

    lesson = get_object_or_404(Lesson, id=lesson_id, owner=request.user)

    lesson.name = request.POST.get('name', lesson.name)
    lesson.description = request.POST.get('description', lesson.description)
    lesson.video_url = request.POST.get('video_url', lesson.video_url)
    lesson.order = int(request.POST.get('order', lesson.order) or lesson.order)
    lesson.save()

    return render(request, 'lms/teacher/partials/lesson_row.html', {
        'lesson': lesson,
    })


@teacher_required
def teacher_lesson_delete(request, lesson_id):
    """Удаление урока (HTMX)."""
    if request.method != 'DELETE':
        return HttpResponse(status=405)

    lesson = get_object_or_404(Lesson, id=lesson_id, owner=request.user)
    lesson.delete()

    return HttpResponse('')


# ============================================================
# ПРЕДПРОСМОТР УРОКА
# ============================================================

@teacher_required
def teacher_lesson_preview(request, lesson_id):
    """Предпросмотр урока глазами ученика."""
    lesson = get_object_or_404(Lesson, id=lesson_id, owner=request.user)

    class FakeProgress:
        is_completed = False

    return render(request, 'lms/student/lesson_detail.html', {
        'lesson': lesson,
        'progress': FakeProgress(),
        'submission': None,
        'is_preview': True,
    })


# ============================================================
# ВОПРОСЫ КОНТРОЛЬНОЙ
# ============================================================

@teacher_required
def teacher_test_questions(request, lesson_id):
    """Список вопросов контрольной."""
    lesson = get_object_or_404(Lesson, id=lesson_id, owner=request.user)

    if not lesson.is_test:
        messages.error(request, 'Этот урок не является контрольной работой')
        return redirect('lms:teacher_course_detail', course_id=lesson.course.id)

    questions = lesson.questions.prefetch_related('answers').all()

    return render(request, 'lms/teacher/test_questions.html', {
        'lesson': lesson,
        'questions': questions,
    })


@teacher_required
def teacher_test_question_create(request, lesson_id):
    """Создание вопроса."""
    lesson = get_object_or_404(Lesson, id=lesson_id, owner=request.user)

    if not lesson.is_test:
        messages.error(request, 'Этот урок не является контрольной работой')
        return redirect('lms:teacher_course_detail', course_id=lesson.course.id)

    if request.method == 'POST':
        text = request.POST.get('text')
        question_type = request.POST.get('question_type', 'single')
        points = int(request.POST.get('points', 1) or 1)
        order = int(request.POST.get('order', 0) or 0)

        if text:
            q = TestQuestion.objects.create(
                lesson=lesson,
                text=text,
                question_type=question_type,
                points=points,
                order=order,
            )

            if question_type in ('single', 'multiple'):
                answers = request.POST.getlist('answer_text')
                correct_indexes = request.POST.getlist('answer_correct')

                for i, ans_text in enumerate(answers):
                    if ans_text.strip():
                        TestAnswer.objects.create(
                            question=q,
                            text=ans_text.strip(),
                            is_correct=(str(i) in correct_indexes),
                            order=i,
                        )

            messages.success(request, 'Вопрос добавлен')
            return redirect('lms:teacher_test_questions', lesson_id=lesson.id)

    return render(request, 'lms/teacher/test_question_form.html', {
        'lesson': lesson,
    })


@teacher_required
def teacher_test_question_delete(request, question_id):
    """Удаление вопроса."""
    if request.method != 'DELETE':
        return HttpResponse(status=405)

    question = get_object_or_404(
        TestQuestion,
        id=question_id,
        lesson__owner=request.user,
    )
    question.delete()

    return HttpResponse('')


# ============================================================
# ПРОВЕРКА РАБОТ
# ============================================================

@teacher_required
def teacher_submissions_list(request):
    """Список работ учеников на проверку."""
    teacher = request.user

    submissions = Submission.objects.filter(
        lesson__course__owner=teacher,
    ).select_related('student', 'lesson', 'lesson__course').order_by('-submitted_at')

    status_filter = request.GET.get('status')
    if status_filter:
        submissions = submissions.filter(status=status_filter)

    return render(request, 'lms/teacher/submissions_list.html', {
        'submissions': submissions,
        'status_filter': status_filter,
    })


@teacher_required
def teacher_check_submission(request, submission_id):
    """Проверка работы ученика."""
    submission = get_object_or_404(
        Submission,
        id=submission_id,
        lesson__course__owner=request.user,
    )

    student_answers = submission.answers.select_related('question').prefetch_related(
        'selected_answers'
    )

    if request.method == 'POST':
        total_score = 0
        has_questions = student_answers.exists()

        if has_questions:
            for sa in student_answers:
                points = request.POST.get(f'points_{sa.id}')
                if points is not None:
                    sa.points_earned = int(points)
                    sa.is_correct = request.POST.get(f'correct_{sa.id}') == 'on'
                    sa.save()
                    total_score += sa.points_earned

        manual_score = request.POST.get('score')
        if manual_score and not has_questions:
            total_score = int(manual_score)

        submission.score = total_score
        submission.teacher_comment = request.POST.get('teacher_comment', '')
        submission.status = 'checked'
        submission.save()

        messages.success(request, 'Оценка выставлена')
        return redirect('lms:teacher_submissions')

    return render(request, 'lms/teacher/check_submission.html', {
        'submission': submission,
        'student_answers': student_answers,
    })


@teacher_required
def teacher_toggle_progress(request, course_id, student_id, lesson_id):
    """Учитель отмечает урок пройденным/не пройденным для ученика."""
    if request.method != 'POST':
        return HttpResponse(status=405)

    course = get_object_or_404(Course, id=course_id, owner=request.user)
    student = get_object_or_404(User, id=student_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)

    # Проверяем, что ученик записан на курс
    if not Subscription.objects.filter(user=student, course=course).exists():
        messages.error(request, 'Ученик не записан на этот курс')
        return redirect('lms:teacher_course_detail', course_id=course.id)

    # Переключаем статус
    progress, created = LessonProgress.objects.get_or_create(
        student=student,
        lesson=lesson
    )

    if progress.is_completed:
        progress.is_completed = False
        progress.completed_at = None
    else:
        progress.is_completed = True
        progress.completed_at = timezone.now()

    progress.save()
    return redirect('lms:teacher_course_detail', course_id=course.id)


@teacher_required
def teacher_course_detail(request, course_id):
    """Детальная страница курса для учителя."""
    teacher = request.user
    course = get_object_or_404(Course, id=course_id, owner=teacher)

    lessons = course.lessons.all().order_by('order', 'id')

    students = User.objects.filter(
        subscriptions__course=course
    ).annotate(
        completed_lessons=Count(
            'progress',
            filter=Q(progress__lesson__course=course, progress__is_completed=True)
        )
    )

    # Добавляем ID пройденных уроков для каждого ученика
    for student in students:
        # Получаем ID всех пройденных уроков этого ученика на данном курсе
        completed_ids = LessonProgress.objects.filter(
            student=student,
            lesson__course=course,
            is_completed=True
        ).values_list('lesson_id', flat=True)
        student.completed_lesson_ids = list(completed_ids)

    return render(request, 'lms/teacher/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'students': students,
    })
