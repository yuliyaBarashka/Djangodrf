# 🎓 M2Bilingual — LMS платформа онлайн-школы иностранных языков

[![Django](https://img.shields.io/badge/Django-6.0.8-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.18.0-red.svg)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/JWT-SimpleJWT-blue.svg)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Celery](https://img.shields.io/badge/Celery-5.6.3-brightgreen.svg)](https://docs.celeryq.dev/)
[![Stripe](https://img.shields.io/badge/Stripe-Integration-purple.svg)](https://stripe.com)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docs.docker.com/compose/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black.svg)](https://github.com/features/actions)

## 📋 Описание

**M2Bilingual** — LMS (Learning Management System) для онлайн-школы иностранных языков.
Полноценный бэкенд с REST API, JWT-авторизацией, Docker-контейнеризацией, CI/CD и автоматическим деплоем на VPS.

**Live Demo:**
- 🌐 **Сайт:** http://51.250.20.108/
- 🎓 **Главная:** http://51.250.20.108/
- 📝 **Форма заявки:** http://51.250.20.108/contact/
- 🔐 **Дашборд сотрудника:** http://51.250.20.108/dashboard/login/
- ⚙️ **Django Admin:** http://51.250.20.108/admin/
- 📚 **API Swagger:** http://51.250.20.108/api/docs/swagger/
- 📖 **API ReDoc:** http://51.250.20.108/api/docs/redoc/

---

## 🚀 Основные возможности

### 👤 Пользователи
- ✅ Кастомная модель User с авторизацией по email
- ✅ JWT-аутентификация (access + refresh tokens)
- ✅ Роли: пользователь, модератор, менеджер, администратор
- ✅ Разграничение прав доступа
- ✅ Роли: учитель (`is_teacher`), ученик (`is_student`)
- ✅ Прогресс ученика: `LessonProgress`, `CourseProgress`

### 📚 Курсы и уроки
- ✅ CRUD для курсов и уроков
- ✅ Валидация YouTube-ссылок
- ✅ Подсчёт уроков в курсе
- ✅ Вложенный вывод уроков

### 🎓 Кабинет ученика (`/student/`)
- ✅ Список курсов, на которые подписан
- ✅ Прогресс по каждому курсу (%)
- ✅ Детальная страница курса с уроками
- ✅ Отметка урока «Пройден» (HTMX, без перезагрузки)
- ✅ Профиль со статистикой

### 👨‍🏫 Кабинет учителя (`/teacher/`)
- ✅ Свои курсы со статистикой (ученики, уроки)
- ✅ Управление уроками: создание, редактирование (inline HTMX), удаление
- ✅ Список учеников по курсам
- ✅ Создание курсов

### 💳 Платежи (Stripe)
- ✅ Создание продуктов и цен в Stripe
- ✅ Checkout-сессии для оплаты
- ✅ Сохранение статуса платежа

### 📨 Форма заявки
- ✅ Отдельная страница `/contact/`
- ✅ Отправка на **Email** (Gmail SMTP)
- ✅ Сохранение в БД (`ContactRequest`)
- ✅ Honeypot-защита от ботов
- ✅ Админ-панель для менеджеров

### 📊 Дашборд сотрудника
- ✅ Отдельная панель `/dashboard/`
- ✅ Кастомный вход для менеджеров
- ✅ Статистика заявок (всего, обработано, новых, за сегодня)
- ✅ Список заявок с фильтрами и поиском
- ✅ Просмотр и отметка «Обработано»
- ✅ Красивый UI (Electric style)

### ⚡ Фоновые задачи (Celery)
- ✅ Асинхронная отправка уведомлений
- ✅ Периодическая блокировка неактивных пользователей
- ✅ Celery Beat для расписания

### 🐳 DevOps
- ✅ Docker Compose (6 сервисов)
- ✅ Nginx reverse proxy
- ✅ CI/CD на GitHub Actions (lint → test → build → deploy)
- ✅ Автоматический деплой на VPS

### 📖 Документация
- ✅ Swagger UI (OpenAPI 3.0)
- ✅ ReDoc
- ✅ Полное описание всех эндпоинтов

---

## 🛠 Технологический стек

| Компонент | Технология | Версия |
|-----------|-----------|--------|
| **Backend** | Django | 6.0.8 |
| **API** | Django REST Framework | 3.18.0 |
| **Аутентификация** | SimpleJWT | 5.5.1 |
| **Документация** | drf-spectacular | 0.30.0 |
| **Платежи** | Stripe | 15.5.0 |
| **Очереди** | Celery | 5.6.3 |
| **Брокер** | Redis | 8.1.0 |
| **БД** | PostgreSQL | 15 |
| **Веб-сервер** | Nginx | Alpine |
| **Контейнеризация** | Docker Compose | 3.8+ |
| **CI/CD** | GitHub Actions | — |
| **ОС сервера** | Ubuntu | 24.04 LTS |
| **HTMX** | 1.9.10 | Динамические интерфейсы без перезагрузки |


---

## 📦 Установка и запуск

### Требования

- Python 3.12+
- Docker Desktop
- Git

### 1. Клонирование репозитория

```bash
git clone https://github.com/yuliyaBarashka/Djangodrf.git
cd Djangodrf
```

### 2. Создание .env

#### Заполни .env:
env:
```dotenv
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=51.250.20.108,m2bilingual.ru,www.m2bilingual.ru,localhost,127.0.0.1

# CSRF
CSRF_TRUSTED_ORIGINS=http://localhost,http://localhost:8000,http://127.0.0.1,http://127.0.0.1:8000,http://51.250.20.108,http://m2bilingual.ru,http://www.m2bilingual.ru
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False

# Database
POSTGRES_DB=m2bilingual_db
POSTGRES_USER=m2bilingual_user
POSTGRES_PASSWORD=StrongPassword2026!
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Email (Gmail)
EMAIL_HOST_USER=zohn12333@gmail.com
EMAIL_HOST_PASSWORD=xxxx xxxx xxxx xxxx

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

### 3. Запуск через Docker Compose

```bash
docker compose up -d --build 
```

#### Все 6 сервисов запустятся:

- db — PostgreSQL  
- redis — Redis  
- app — Django + Gunicorn  
- celery — Celery Worker  
- celerybeat — Celery Beat  
- nginx — Reverse proxy  

### 4. Проверка

```bash
docker compose ps
```
#### Все контейнеры должны быть Up.  

### 5. Создание суперпользователя

```bash
docker compose exec app python manage.py createsuperuser
```

#### Введи:

- Email: admin@example.com
- Password: (свой) не менее 8 символов

### 6. Открой в браузере

- Сайт: http://localhost/
- Админка: http://localhost/admin/
- Дашборд: http://localhost/dashboard/login/
- API: http://localhost/api/

## 🎯 API Эндпоинты

### Аутентификация

| Метод | URL | Описание | Доступ |
|-------|-----|----------|--------|
| POST | `/api/register/` | Регистрация | Все |
| POST | `/api/token/` | Получить JWT | Все |
| POST | `/api/token/refresh/` | Обновить JWT | Все |

### Пользователи

| Метод | URL | Описание | Доступ |
|-------|-----|----------|--------|
| GET | `/api/users/` | Список | Admin |
| GET | `/api/users/{id}/` | Профиль | Auth |
| PUT/PATCH | `/api/users/{id}/` | Обновить | Владелец |
| DELETE | `/api/users/{id}/` | Удалить | Владелец |

### Курсы

| Метод | URL | Описание | Доступ |
|-------|-----|----------|--------|
| GET | `/api/courses/` | Список | Auth |
| POST | `/api/courses/` | Создать | Не модератор |
| GET/PUT/PATCH/DELETE | `/api/courses/{id}/` | CRUD | Модератор/Владелец |

### Уроки

| Метод | URL | Описание | Доступ |
|-------|-----|----------|--------|
| GET | `/api/lessons/` | Список | Auth |
| POST | `/api/lessons/create/` | Создать | Не модератор |
| GET | `/api/lessons/{id}/` | Просмотр | Auth |
| PUT/PATCH | `/api/lessons/{id}/update/` | Обновить | Модератор/Владелец |
| DELETE | `/api/lessons/{id}/delete/` | Удалить | Владелец |

### Подписки и платежи

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/api/subscriptions/` | Подписка/отписка |
| POST | `/api/payments/create/` | Создать платёж (Stripe) |
| GET | `/api/payments/status/` | Статус платежа |
| GET | `/api/payments/` | Список платежей |

### HTML-страницы (кабинеты)

| URL | Описание | Доступ |
|-----|----------|--------|
| `/login/` | Вход | Все |
| `/logout/` | Выход | Auth |
| `/student/` | Кабинет ученика | Student |
| `/student/course/{id}/` | Курс ученика | Student |
| `/student/lesson/{id}/` | Урок ученика | Student |
| `/teacher/` | Кабинет учителя | Teacher |
| `/teacher/course/{id}/` | Курс учителя | Teacher |
| `/teacher/students/` | Ученики учителя | Teacher |
| `/teacher/course/create/` | Создать курс | Teacher |

---
## 📊 Дашборд ученика и учителя

### 🧪 Тестовые пользователи

| Роль | Email | Пароль |
|------|-------|--------|
| Учитель | teacher@m2bilingual.ru | Teacher2026! |
| Ученик | student@m2bilingual.ru | Student2026! |

## 📊 Дашборд сотрудника

### URL: `/dashboard/login/`

**Для входа используй:**
- Email: `manager@m2bilingual.ru`
- Password: `ManagerPass2026!`

### Возможности:

- ✅ **Дашборд** — статистика (всего заявок, не обработано, обработано, за сегодня)
- ✅ **Заявки** — список с фильтрами и поиском
- ✅ **Просмотр заявки** — отметить как обработанную
- ❌ **НЕ видит** пользователей, платежи, курсы
- ❌ **НЕ видит** Django Admin (если не суперпользователь)

### Роли:

| Роль | Доступ |
|------|--------|
| **Суперпользователь** | Django Admin + Дашборд + всё |
| **Managers** (группа) | Только Дашборд и Заявки |
| **Обычный пользователь** | Только API |

---

## 🧪 Тестирование

### Запуск тестов

```bash
docker compose exec app python manage.py test
#С покрытием
docker compose exec app coverage run --source='.' manage.py test
docker compose exec app coverage report
docker compose exec app coverage html
```

## 🐳 Docker

```bash
# Запустить
docker compose up -d

# Пересобрать
docker compose up -d --build

# Пересоздать контейнеры
docker compose up -d --force-recreate

# Остановить
docker compose down

# Логи
docker compose logs --tail=50 app

# Зайти в контейнер
docker compose exec app bash

# Django shell
docker compose exec app python manage.py shell
```

## 🚀 CI/CD

### GitHub Actions

При push в main запускается workflow:
1. 🔍 Lint — flake8
2. 🧪 Test — тесты с PostgreSQL + Redis
3. 🐳 Build — сборка Docker-образов
4. 🚀 Deploy — автодеплой на VPS

### Секреты в GitHub

SSH_HOST=  
SSH_USER=deploy  
SSH_KEY=Приватный SSH-ключ  
SSH_PORT=  
DEPLOY_DIR=  
DJANGO_SECRET_KEY=Django SECRET_KEY  
DB_NAME=  
DB_USER=  
DB_PASSWORD=  
DB_HOST=  
DB_PORT=  
REDIS_URL=  
CELERY_BROKER_URL=  
CELERY_RESULT_BACKEND=  
EMAIL_HOST_USER=  
EMAIL_HOST_PASSWORD=  
STRIPE_PUBLISHABLE_KEY=  
STRIPE_SECRET_KEY=  

## 🖥 Деплой на VPS

### Требования

- Ubuntu 24.04 LTS
- Docker + Docker Compose
- SSH-доступ
- PostgreSQL, Redis (в Docker)

## 📁 Структура проекта

```text
Djangodrf/
│
├── .github/
│   └── workflows/
│       └── ci.yml                          # CI/CD: lint → test → build → deploy
│
├── config/                                 # Настройки Django-проекта
│   ├── __init__.py
│   ├── celery.py                           # Celery app
│   ├── settings.py                         # Настройки (INSTALLED_APPS, БД, JWT, Stripe)
│   ├── urls.py                             # ✅ ИСПРАВЛЕН: без дублей, с users.urls_auth и lms.urls_cabinet
│   ├── wsgi.py
│   └── asgi.py                             # (если есть)
│
├── core/                                   # Главная + форма заявки
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py                            # ContactForm (с consent)
│   ├── migrations/
│   ├── models.py                           # ContactRequest
│   ├── urls.py                             # /, /contact/, /privacy/, /consent/
│   ├── utils.py                            # send_email_notification
│   └── views.py                            # index, contact, privacy_policy, consent
│
├── dashboard/                              # Дашборд сотрудника
│   ├── __init__.py
│   ├── decorators.py                       # manager_required
│   ├── templates/
│   │   └── dashboard/
│   │       ├── base.html
│   │       ├── login.html
│   │       ├── index.html
│   │       ├── requests.html
│   │       └── request_detail.html
│   ├── urls.py
│   └── views.py                            # index, requests_list, request_detail
│
├── lms/                                    # Курсы, уроки, подписки
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── models.py                           # Course, Lesson, Subscription
│   ├── paginators.py
│   ├── serializers.py
│   ├── services.py                         # Stripe-интеграция
│   ├── tasks.py                            # Celery-задачи
│   ├── urls.py                             # API: /api/courses/, /api/lessons/, ...
│   ├── urls_cabinet.py                     # 🆕 HTML: /student/, /teacher/
│   ├── validators.py                       # YouTube-валидация
│   ├── views.py                            # API-views (CourseViewSet, Lesson*APIView, ...)
│   ├── views_student.py                    # 🆕 Кабинет ученика
│   └── views_teacher.py                    # 🆕 Кабинет учителя
│
├── users/                                  # Пользователи, платежи, прогресс
│   ├── __init__.py                         # ⚠️ ДОЛЖЕН БЫТЬ ПУСТЫМ (без импортов!)
│   ├── admin.py
│   ├── apps.py
│   ├── decorators.py                       # 🆕 student_required, teacher_required
│   ├── fixtures/
│   ├── management/
│   ├── migrations/
│   ├── models.py                           # User, Payment, LessonProgress, CourseProgress
│   ├── permissions.py                      # IsModerator, IsOwner
│   ├── serializers.py
│   ├── tasks.py
│   ├── tests.py
│   ├── urls.py                             # API: /api/users/, /api/register/, ...
│   ├── urls_auth.py                        # 🆕 HTML: /login/, /logout/
│   └── views.py                            # ✅ login_view, logout_view + API-views
│
├── templates/                              # HTML-шаблоны
│   ├── core/
│   │   ├── index.html                      # ✅ С кнопками «Войти» / «Кабинет»
│   │   ├── contact.html
│   │   ├── privacy.html
│   │   └── consent.html
│   │
│   ├── users/
│   │   └── login.html                      # 🆕 Форма входа (email + password)
│   │
│   └── lms/
│       ├── student/                        # 🆕 Кабинет ученика
│       │   ├── base_student.html           # базовый шаблон с sidebar + HTMX
│       │   ├── dashboard.html              # список курсов с прогрессом
│       │   ├── course_detail.html          # уроки курса + отметка «пройден»
│       │   ├── lesson_detail.html          # страница урока
│       │   ├── profile.html                # профиль ученика
│       │   └── partials/
│       │       └── lesson_status.html      # HTMX-фрагмент (статус урока)
│       │
│       └── teacher/                        # 🆕 Кабинет учителя
│           ├── base_teacher.html           # базовый шаблон с sidebar + HTMX
│           ├── dashboard.html              # список своих курсов
│           ├── course_detail.html          # уроки + ученики
│           ├── students.html               # список учеников
│           ├── create_course.html          # форма создания курса
│           ├── create_lesson.html          # форма создания урока
│           └── partials/
│               ├── lesson_row.html         # HTMX-строка урока
│               └── lesson_edit_form.html   # HTMX-форма редактирования
│
├── static/                                 # Статика
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── main.js
│   │   └── htmx.min.js                     # 🆕 (если скачан локально)
│   └── images/
│       └── hero-bg.jpeg
│
├── staticfiles/                            # collectstatic (volume)
├── media/                                  # Загруженные файлы (volume)
│   └── users/avatars/
│
├── fixtures/                               # Тестовые данные
├── htmlcov/                                # coverage HTML
├── venv/                                   # (не должно быть в образе)
│
├── .env                                    # Переменные окружения (не в git)
├── .env.sample
├── .env.docker.sample
├── .gitignore
├── Dockerfile
├── docker-compose.yml                      # 6 сервисов
├── nginx.conf
├── manage.py
├── requirements.txt
├── pyproject.toml
├── poetry.lock
├── coverage.txt
├── main.py                                 
└──README.md
```

## 👨‍💻 Автор

Юлия Тихонова

- GitHub: @yuliyaBarashka
- Email: zohn12333@gmail.com











