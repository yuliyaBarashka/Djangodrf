# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем необходимые системные пакеты
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements.txt и устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь код проекта в контейнер
COPY . .

# Создаем директории для статики и медиа
RUN mkdir -p /app/static /app/media

# Открываем порт 8000
EXPOSE 8000

# Команда запуска (переопределяется в docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]