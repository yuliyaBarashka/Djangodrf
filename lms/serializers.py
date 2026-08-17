from rest_framework import serializers
from lms.models import Course, Lesson, Subscription
from lms.validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'description', 'preview', 'video_url', 'course', 'owner']
        read_only_fields = ['owner']

    def validate_video_url(self, value):
        if value:
            validate_youtube_url(value)
        return value


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()  # Поле для проверки подписки

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lessons_count', 'lessons', 'owner', 'is_subscribed']
        read_only_fields = ['owner']

    def get_lessons_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        """Проверяет, подписан ли текущий пользователь на курс"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=obj
            ).exists()
        return False


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки"""
    course_name = serializers.CharField(source='course.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'user_email', 'course', 'course_name', 'created_at']
        read_only_fields = ['user', 'created_at']