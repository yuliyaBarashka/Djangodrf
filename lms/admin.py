from django.contrib import admin
from lms.models import (
    Course, Lesson, Subscription, Submission,
    TestQuestion, TestAnswer, StudentAnswer,
)


# ============================================================
# ИНЛАЙНЫ
# ============================================================

class SubscriptionInline(admin.TabularInline):
    """Подписки (ученики) прямо на странице курса."""
    model = Subscription
    extra = 1
    autocomplete_fields = ['user']
    verbose_name = 'Ученик на курсе'
    verbose_name_plural = 'Ученики на курсе'


class LessonInline(admin.TabularInline):
    """Уроки прямо на странице курса."""
    model = Lesson
    extra = 0
    fields = ('order', 'name', 'is_test', 'video_url')
    show_change_link = True


class TestAnswerInline(admin.TabularInline):
    """Варианты ответа на странице вопроса."""
    model = TestAnswer
    extra = 4
    fields = ('order', 'text', 'is_correct')


# ============================================================
# КУРС
# ============================================================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'owner', 'price', 'is_published',
        'students_count', 'lessons_count', 'updated_at',
    )
    list_filter = ('is_published', 'owner')
    search_fields = ('name', 'description')
    readonly_fields = ('updated_at', 'stripe_product_id')
    inlines = [LessonInline, SubscriptionInline]

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'description', 'preview', 'owner')
        }),
        ('Цена и публикация', {
            'fields': ('price', 'is_published')
        }),
        ('Stripe', {
            'fields': ('stripe_product_id',),
            'classes': ('collapse',),
        }),
        ('Даты', {
            'fields': ('updated_at',),
        }),
    )

    def students_count(self, obj):
        return obj.subscribers.count()
    students_count.short_description = 'Учеников'

    def lessons_count(self, obj):
        return obj.lessons.count()
    lessons_count.short_description = 'Уроков'


# ============================================================
# УРОК
# ============================================================

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'course', 'order',
        'is_test', 'has_video', 'has_lecture', 'has_workbook',
    )
    list_filter = ('is_test', 'course')
    search_fields = ('name', 'description')
    list_editable = ('order',)
    autocomplete_fields = ['course']
    readonly_fields = ('updated_at',)

    fieldsets = (
        ('Основное', {
            'fields': ('course', 'name', 'description', 'preview', 'order')
        }),
        ('Видео', {
            'fields': ('video_url',)
        }),
        ('Материалы', {
            'fields': ('lecture_pdf', 'workbook_pdf')
        }),
        ('Контрольная работа', {
            'fields': ('is_test', 'test_file', 'max_score'),
            'classes': ('collapse',),
        }),
        ('Служебное', {
            'fields': ('owner', 'updated_at'),
        }),
    )

    def has_video(self, obj):
        return bool(obj.video_url)
    has_video.boolean = True
    has_video.short_description = '📹'

    def has_lecture(self, obj):
        return bool(obj.lecture_pdf)
    has_lecture.boolean = True
    has_lecture.short_description = '📄'

    def has_workbook(self, obj):
        return bool(obj.workbook_pdf)
    has_workbook.boolean = True
    has_workbook.short_description = '📝'


# ============================================================
# ПОДПИСКА (ученик ↔ курс)
# ============================================================

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'course', 'created_at')
    list_filter = ('course',)
    search_fields = ('user__email', 'course__name')
    autocomplete_fields = ['user', 'course']
    date_hierarchy = 'created_at'


# ============================================================
# РАБОТА УЧЕНИКА
# ============================================================

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'student', 'lesson', 'status',
        'submitted_at', 'score',
    )
    list_filter = ('status', 'lesson__course')
    search_fields = ('student__email', 'lesson__name')
    autocomplete_fields = ['student', 'lesson']
    readonly_fields = ('created_at', 'updated_at')


# ============================================================
# ВОПРОСЫ КОНТРОЛЬНОЙ
# ============================================================

@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'lesson', 'short_text', 'question_type', 'points', 'order')
    list_filter = ('question_type', 'lesson__course')
    search_fields = ('text', 'lesson__name')
    autocomplete_fields = ['lesson']
    list_editable = ('order', 'points')
    inlines = [TestAnswerInline]

    def short_text(self, obj):
        return obj.text[:60]
    short_text.short_description = 'Вопрос'


@admin.register(TestAnswer)
class TestAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'text', 'is_correct', 'order')
    list_filter = ('is_correct',)
    search_fields = ('text',)
    autocomplete_fields = ['question']


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'question', 'is_correct', 'points_earned')
    list_filter = ('is_correct',)
    search_fields = ('submission__student__email',)
    autocomplete_fields = ['submission', 'question']
    