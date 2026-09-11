import os
from celery import Celery
from celery.schedules import crontab

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создаем приложение Celery
app = Celery('config')

# Загружаем настройки из Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматически находим задачи в приложениях
app.autodiscover_tasks()

# Настройка периодических задач (Celery Beat)
app.conf.beat_schedule = {
    # Задача 3: Блокировка неактивных пользователей (ежедневно в полночь)
    'block-inactive-users': {
        'task': 'users.tasks.block_inactive_users',
        'schedule': crontab(hour=0, minute=0),  # Каждый день в полночь
        'args': (),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    