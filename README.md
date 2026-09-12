# 🎓 LMS System API

[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14.0-red.svg)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/JWT-SimpleJWT-blue.svg)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Stripe](https://img.shields.io/badge/Stripe-Integration-purple.svg)](https://stripe.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Описание

LMS (Learning Management System) API — это бэкенд для платформы онлайн-обучения с полным функционалом управления курсами, уроками, пользователями, подписками и платежами через Stripe.

**Техническое задание:** Создание SPA веб-приложения с бэкенд-сервером, возвращающим JSON-структуры.

---

## 🚀 Основные возможности

### 👤 Пользователи
- ✅ Регистрация и аутентификация через JWT
- ✅ CRUD операции с пользователями
- ✅ Разграничение ролей: пользователь, модератор, администратор
- ✅ Профиль пользователя с историей платежей

### 📚 Курсы и уроки
- ✅ Полный CRUD для курсов и уроков
- ✅ Валидация видео-ссылок (только YouTube)
- ✅ Подсчет количества уроков в курсе
- ✅ Вложенный вывод уроков в курсе

### 🔐 Права доступа
- ✅ Модератор: просмотр и редактирование, но без создания/удаления
- ✅ Владелец: полный контроль над своими объектами
- ✅ Обычный пользователь: только свои объекты
- ✅ JWT авторизация с refresh токенами

### 💳 Платежи
- ✅ Интеграция с Stripe (тестовый режим)
- ✅ Создание продуктов и цен в Stripe
- ✅ Checkout сессии для оплаты
- ✅ Сохранение статуса платежа
- ✅ Webhook обработка (опционально)
- ✅ История платежей пользователя

### 📖 Документация
- ✅ Swagger UI (OpenAPI 3.0)
- ✅ ReDoc
- ✅ Полное описание всех эндпоинтов

---

## 🛠 Технологический стек

| Компонент | Технология | Версия |
|-----------|-----------|--------|
| Backend | Django | 4.2.7 |
| API Framework | Django REST Framework | 3.14.0 |
| Аутентификация | JWT (SimpleJWT) | 5.3.0 |
| Документация | drf-spectacular | 0.27.0 |
| Платежи | Stripe API | Latest |
| База данных | SQLite (dev) / PostgreSQL (prod) | - |
| Переменные окружения | python-dotenv | 1.0.0 |

---

## 📦 Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <repository-url>
cd Djangodrf

python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# или
venv\Scripts\activate  # Windows  

pip install -r requirements.txt  
```
Настройка переменных окружения

Создайте файл .env в корне проекта на основе файла .env.sample  

### Применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание суперпользователя
```bash
python manage.py createsuperuser
```

### Загрузка фикстур
```bash
python manage.py loaddata fixtures/data.json
python manage.py loaddata users/fixtures/groups.json
```

### Запуск сервера
```bash
python manage.py runserver
```
## Структура проекта
Djangodrf/  
├── config/                     # Настройки проекта  
│   ├── settings.py  
│   ├── urls.py  
│   └── wsgi.py  
├── users/                      # Приложение пользователей  
│   ├── models.py              # User, Payment  
│   ├── serializers.py  
│   ├── views.py  
│   ├── urls.py  
│   ├── permissions.py         # IsModerator, IsOwner  
│   └── fixtures/  
│       └── groups.json        # Группа модераторов  
├── lms/                       # Приложение LMS  
│   ├── models.py              # Course, Lesson, Subscription  
│   ├── serializers.py  
│   ├── views.py   
│   ├── urls.py  
│   ├── services.py            # Stripe интеграция  
│   ├── validators.py          # YouTube валидатор  
│   └── paginators.py          # Пагинация    
├── fixtures/    
│   └── data.json              # Тестовые данные  
├── media/                     # Загруженные файлы    
├── .env                       # Переменные окружения  
├── manage.py  
├── requirements.txt  
└── README.md  


## ⚡ Celery + Redis

### Запуск Celery

```bash
# Запуск worker
celery -A config worker --loglevel=info

# Запуск beat (для периодических задач)
celery -A config beat --loglevel=info

# Запуск обоих в одном терминале
celery -A config worker --loglevel=info --beat
```
## 🐳 Запуск через Docker Compose

### 1. Подготовка

```bash
# Скопировать переменные окружения
cp .env.docker.sample .env

# Отредактировать .env при необходимости
nano .env
# Собрать и запустить все контейнеры
docker-compose up --build -d

# Проверить статус
docker-compose ps

# Посмотреть логи
docker-compose logs -f app celery_worker celery_beat
docker-compose exec app python manage.py createsuperuser
docker-compose down

# Остановка с удалением томов (очистка данных)
docker-compose down -v
```
## Доступ к приложению

API: http://localhost:8000/api/
Админка: http://localhost:8000/admin/
Swagger: http://localhost:8000/api/docs/swagger/


## 🌐 Production

Приложение развёрнуто на VPS: **http://51.250.20.108/**  
  
- **Админка:** http://51.250.20.108/admin/  
- **API:** http://51.250.20.108/api/  
- **Swagger:** http://51.250.20.108/api/docs/swagger/  
  
### CI/CD
  
При push в `main` или `develop`:  
1. Запускается линтинг (flake8)  
2. Запускаются тесты (с PostgreSQL + Redis)  
3. Выполняется автоматический деплой на VPS через SSH  
  
Секреты настраиваются в GitHub: `SSH_HOST`, `SSH_USER`, `SSH_KEY`, `SSH_PORT`, `DEPLOY_DIR` и др.  
