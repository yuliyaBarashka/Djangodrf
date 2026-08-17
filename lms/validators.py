import re
from django.core.exceptions import ValidationError


def validate_youtube_url(value):
    """
    Валидатор для проверки, что ссылка ведет на YouTube
    """
    # Паттерн для YouTube URL
    youtube_pattern = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'

    if not re.match(youtube_pattern, value):
        raise ValidationError(
            'Разрешены только ссылки на YouTube (youtube.com или youtu.be)'
        )

    return value
