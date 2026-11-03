from rest_framework import serializers
from lms.models import Course, Lesson, Subscription, Submission
from lms.validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    youtube_embed_url = serializers.ReadOnlyField()

    class Meta:
        model = Lesson
        fields = [
            'id', 'name', 'description', 'preview',
            'order',
            'video_url', 'youtube_embed_url',
            'lecture_pdf', 'workbook_pdf',
            'is_test', 'test_file', 'max_score',
            'course', 'owner',
        ]
        read_only_fields = ['owner']

    def validate_video_url(self, value):
        if value:
            validate_youtube_url(value)
        return value


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'name', 'preview', 'description',
            'price', 'is_published',
            'lessons_count', 'lessons', 'owner', 'is_subscribed',
        ]
        read_only_fields = ['owner']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user, course=obj
            ).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'user_email', 'course', 'course_name', 'created_at']
        read_only_fields = ['user', 'created_at']


class SubmissionSerializer(serializers.ModelSerializer):
    """Сериализатор работы ученика."""
    student_email = serializers.CharField(source='student.email', read_only=True)
    lesson_name = serializers.CharField(source='lesson.name', read_only=True)

    class Meta:
        model = Submission
        fields = [
            'id', 'student', 'student_email',
            'lesson', 'lesson_name',
            'file', 'status', 'submitted_at',
            'score', 'teacher_comment',
            'created_at', 'updated_at',
        ]
        read_only_fields = [
            'student', 'status', 'submitted_at',
            'score', 'teacher_comment',
            'created_at', 'updated_at',
        ]