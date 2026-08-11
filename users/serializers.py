from rest_framework import serializers
from users.models import User, Payment
from lms.serializers import CourseSerializer, LessonSerializer


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей"""

    # Для отображения названий курсов и уроков
    course_name = serializers.CharField(source='course.name', read_only=True)
    lesson_name = serializers.CharField(source='lesson.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'user_email', 'payment_date',
            'course', 'course_name', 'lesson', 'lesson_name',
            'amount', 'payment_method'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя с историей платежей"""

    # Вложенный список платежей пользователя (* Дополнительное задание)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone', 'city', 'avatar',
            'first_name', 'last_name', 'payments'
        ]
        