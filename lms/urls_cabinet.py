from django.urls import path
from lms import views_student, views_teacher

app_name = 'lms'

urlpatterns = [
    # ===== ПУБЛИЧНОЕ =====
    path('courses/<int:course_id>/',
         views_student.course_preview,
         name='course_preview'),

    # ===== КАБИНЕТ УЧЕНИКА =====
    path('student/',
         views_student.student_dashboard,
         name='student_dashboard'),
    path('student/course/<int:course_id>/',
         views_student.student_course_detail,
         name='student_course_detail'),
    path('student/lesson/<int:lesson_id>/',
         views_student.student_lesson_detail,
         name='student_lesson_detail'),
    path('student/lesson/<int:lesson_id>/complete/',
         views_student.mark_lesson_complete,
         name='student_lesson_complete'),
    path('student/lesson/<int:lesson_id>/workbook/',
         views_student.student_submit_workbook,
         name='student_submit_workbook'),
    path('student/lesson/<int:lesson_id>/test/',
         views_student.student_test_start,
         name='student_test_start'),
    path('student/lesson/<int:lesson_id>/test/submit/',
         views_student.student_test_submit,
         name='student_test_submit'),
    path('student/profile/',
         views_student.student_profile,
         name='student_profile'),

    # ===== КАБИНЕТ УЧИТЕЛЯ =====
    path('teacher/',
         views_teacher.teacher_dashboard,
         name='teacher_dashboard'),
    path('teacher/course/<int:course_id>/',
         views_teacher.teacher_course_detail,
         name='teacher_course_detail'),
    path('teacher/students/',
         views_teacher.teacher_students_list,
         name='teacher_students'),
    path('teacher/course/create/',
         views_teacher.teacher_create_course,
         name='teacher_create_course'),
    path('teacher/course/<int:course_id>/lesson/create/',
         views_teacher.teacher_create_lesson,
         name='teacher_create_lesson'),

    # ===== HTMX: РЕДАКТИРОВАНИЕ УРОКА =====
    path('teacher/lesson/<int:lesson_id>/edit/',
         views_teacher.teacher_lesson_edit_form,
         name='teacher_lesson_edit_form'),
    path('teacher/lesson/<int:lesson_id>/update/',
         views_teacher.teacher_lesson_update,
         name='teacher_lesson_update'),
    path('teacher/lesson/<int:lesson_id>/delete/',
         views_teacher.teacher_lesson_delete,
         name='teacher_lesson_delete'),

    # ===== ПРЕДПРОСМОТР УРОКА =====
    path('teacher/lesson/<int:lesson_id>/preview/',
         views_teacher.teacher_lesson_preview,
         name='teacher_lesson_preview'),

    # ===== ВОПРОСЫ КОНТРОЛЬНОЙ =====
    path('teacher/lesson/<int:lesson_id>/questions/',
         views_teacher.teacher_test_questions,
         name='teacher_test_questions'),
    path('teacher/lesson/<int:lesson_id>/questions/create/',
         views_teacher.teacher_test_question_create,
         name='teacher_test_question_create'),
    path('teacher/question/<int:question_id>/delete/',
         views_teacher.teacher_test_question_delete,
         name='teacher_test_question_delete'),

    # ===== ПРОВЕРКА РАБОТ =====
    path('teacher/submissions/',
         views_teacher.teacher_submissions_list,
         name='teacher_submissions'),
    path('teacher/submissions/<int:submission_id>/check/',
         views_teacher.teacher_check_submission,
         name='teacher_check_submission'),
    path('teacher/course/<int:course_id>/student/<int:student_id>/lesson/<int:lesson_id>/toggle/',
         views_teacher.teacher_toggle_progress,
         name='teacher_toggle_progress'),
]