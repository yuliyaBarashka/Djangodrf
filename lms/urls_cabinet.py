from django.urls import path
from lms import views_student, views_teacher

app_name = 'lms'

urlpatterns = [
    # ===== КАБИНЕТ УЧЕНИКА =====
    path('student/', views_student.student_dashboard, name='student_dashboard'),
    path('student/course/<int:course_id>/', views_student.student_course_detail, name='student_course_detail'),
    path('student/lesson/<int:lesson_id>/', views_student.student_lesson_detail, name='student_lesson_detail'),
    path('student/lesson/<int:lesson_id>/complete/', views_student.mark_lesson_complete, name='student_lesson_complete'),
    path('student/profile/', views_student.student_profile, name='student_profile'),

    # ===== КАБИНЕТ УЧИТЕЛЯ =====
    path('teacher/', views_teacher.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/course/<int:course_id>/', views_teacher.teacher_course_detail, name='teacher_course_detail'),
    path('teacher/students/', views_teacher.teacher_students_list, name='teacher_students'),
    path('teacher/course/create/', views_teacher.teacher_create_course, name='teacher_create_course'),
    path('teacher/course/<int:course_id>/lesson/create/', views_teacher.teacher_create_lesson, name='teacher_create_lesson'),

    # HTMX
    path('teacher/lesson/<int:lesson_id>/edit/', views_teacher.teacher_lesson_edit_form, name='teacher_lesson_edit_form'),
    path('teacher/lesson/<int:lesson_id>/update/', views_teacher.teacher_lesson_update, name='teacher_lesson_update'),
    path('teacher/lesson/<int:lesson_id>/delete/', views_teacher.teacher_lesson_delete, name='teacher_lesson_delete'),
]
