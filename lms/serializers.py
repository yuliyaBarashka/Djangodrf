from rest_framework import serializers
from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    # Поле для подсчета количества уроков (Задание 1)
    lessons_count = serializers.SerializerMethodField()

    # Поле для вывода всех уроков курса (Задание 3)
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'preview', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):
        """Метод для подсчета количества уроков в курсе"""
        return obj.lessons.count()