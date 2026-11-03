from django.db import models
from django.conf import settings

from .validators import validate_youtube_url


class Course(models.Model):
    """
    Модель курса.

    Поля:
        name: Название курса
        preview: Превью (картинка)
        description: Описание курса
        price: Цена курса (₽)
        is_published: Опубликован ли курс
        owner: Владелец курса
        stripe_product_id: ID продукта в Stripe
        updated_at: Дата последнего обновления
    """
    name = models.CharField(max_length=200, verbose_name='Название')
    preview = models.ImageField(
        upload_to='courses/previews/',
        blank=True, null=True,
        verbose_name='Превью'
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name='Описание'
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0,
        verbose_name='Цена (₽)'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликован'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='owned_courses',
        verbose_name='Владелец'
    )
    stripe_product_id = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name='ID продукта в Stripe'
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-updated_at']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    Модель урока.

    Урок может содержать (в любой комбинации):
    - YouTube-видео
    - PDF-конспект лекций
    - PDF-рабочая тетрадь
    - Контрольная работа (задания + загрузка решения учеником)
    """
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    preview = models.ImageField(
        upload_to='lessons/previews/',
        blank=True, null=True,
        verbose_name='Превью'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    # ===== Видео =====
    video_url = models.URLField(
        blank=True, null=True,
        validators=[validate_youtube_url],
        verbose_name='Ссылка на YouTube'
    )

    # ===== PDF-материалы =====
    lecture_pdf = models.FileField(
        upload_to='lessons/lectures/',
        blank=True, null=True,
        verbose_name='Конспект лекций (PDF)'
    )
    workbook_pdf = models.FileField(
        upload_to='lessons/workbooks/',
        blank=True, null=True,
        verbose_name='Рабочая тетрадь (PDF)'
    )

    # ===== Контрольная =====
    is_test = models.BooleanField(
        default=False,
        verbose_name='Контрольная работа'
    )
    test_file = models.FileField(
        upload_to='lessons/tests/',
        blank=True, null=True,
        verbose_name='Задания контрольной (PDF)'
    )
    max_score = models.PositiveIntegerField(
        default=100,
        verbose_name='Макс. балл'
    )

    # ===== Связи =====
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Курс'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='owned_lessons',
        verbose_name='Владелец'
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['order', 'id']

    def __str__(self):
        return f'{self.course.name} — {self.name}'

    @property
    def youtube_embed_url(self):
        """Конвертирует YouTube-ссылку в embed-формат для iframe."""
        if not self.video_url:
            return ''
        url = self.video_url

        if 'youtu.be/' in url:
            vid = url.split('youtu.be/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{vid}'
        if 'watch?v=' in url:
            vid = url.split('watch?v=')[1].split('&')[0]
            return f'https://www.youtube.com/embed/{vid}'
        if '/embed/' in url:
            return url
        if '/shorts/' in url:
            vid = url.split('/shorts/')[1].split('?')[0]
            return f'https://www.youtube.com/embed/{vid}'

        return url

    @property
    def has_content(self):
        """Есть ли у урока хоть какой-то контент."""
        return any([
            self.video_url,
            self.lecture_pdf,
            self.workbook_pdf,
            self.is_test,
        ])


class Subscription(models.Model):
    """Подписка на обновления курса (free) или покупка (paid)."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Курс'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    class Meta:
        unique_together = ('user', 'course')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} -> {self.course.name}"


class Submission(models.Model):
    """
    Работа ученика по контрольной.

    Ученик загружает файл → статус 'submitted'.
    Учитель проверяет → статус 'checked', выставляет score и comment.
    """
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('submitted', 'На проверке'),
        ('checked', 'Проверено'),
    ]

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Ученик'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Урок'
    )
    file = models.FileField(
        upload_to='submissions/',
        blank=True, null=True,
        verbose_name='Файл с решением'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Статус'
    )
    submitted_at = models.DateTimeField(
        null=True, blank=True,
        verbose_name='Дата отправки'
    )
    score = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='Оценка'
    )
    teacher_comment = models.TextField(
        blank=True,
        verbose_name='Комментарий учителя'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        unique_together = ('student', 'lesson')
        verbose_name = 'Работа ученика'
        verbose_name_plural = 'Работы учеников'
        ordering = ['-submitted_at', '-created_at']

    def __str__(self):
        return f'{self.student.email} — {self.lesson.name} ({self.get_status_display()})'


class TestQuestion(models.Model):
    QUESTION_TYPES = [
        ('single', 'Один вариант'),
        ('multiple', 'Несколько вариантов'),
        ('text', 'Текстовый ответ'),
        ('file', 'Загрузка файла'),
    ]

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name='Урок'
    )
    text = models.TextField(verbose_name='Вопрос')
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPES,
        default='single',
        verbose_name='Тип вопроса'
    )
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    points = models.PositiveIntegerField(default=1, verbose_name='Баллы')

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Вопрос контрольной'
        verbose_name_plural = 'Вопросы контрольной'

    def __str__(self):
        return f'{self.lesson.name}: {self.text[:50]}'


class TestAnswer(models.Model):
    """Вариант ответа для вопроса (для типов single/multiple)"""
    question = models.ForeignKey(
        TestQuestion,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос'
    )
    text = models.CharField(max_length=500, verbose_name='Вариант')
    is_correct = models.BooleanField(default=False, verbose_name='Правильный')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'

    def __str__(self):
        return self.text[:50]


class StudentAnswer(models.Model):
    """Ответ ученика на конкретный вопрос"""
    submission = models.ForeignKey(
        'Submission',
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Работа'
    )
    question = models.ForeignKey(
        TestQuestion,
        on_delete=models.CASCADE,
        related_name='student_answers',
        verbose_name='Вопрос'
    )
    # Для single/multiple
    selected_answers = models.ManyToManyField(
        TestAnswer,
        blank=True,
        related_name='+',
        verbose_name='Выбранные варианты'
    )
    # Для text
    text_answer = models.TextField(blank=True, verbose_name='Текстовый ответ')
    # Для file
    file_answer = models.FileField(
        upload_to='submissions/files/',
        blank=True, null=True,
        verbose_name='Файл-ответ'
    )
    # Оценка
    is_correct = models.BooleanField(null=True, blank=True, verbose_name='Верно')
    points_earned = models.PositiveIntegerField(default=0, verbose_name='Получено баллов')

    class Meta:
        unique_together = ('submission', 'question')
        verbose_name = 'Ответ ученика'
        verbose_name_plural = 'Ответы учеников'

    def __str__(self):
        return f'{self.submission.student.email} — {self.question.text[:30]}'