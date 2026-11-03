# 🎓 M2Bilingual — LMS for an Online Language School

[![Django](https://img.shields.io/badge/Django-6.0.8-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.18.0-red.svg)](https://www.django-rest-framework.org/)
[![JWT](https://img.shields.io/badge/JWT-SimpleJWT-blue.svg)](https://django-rest-framework-simplejwt.readthedocs.io/)
[![Celery](https://img.shields.io/badge/Celery-5.6.3-brightgreen.svg)](https://docs.celeryq.dev/)
[![Stripe](https://img.shields.io/badge/Stripe-Integration-purple.svg)](https://stripe.com)
[![HTMX](https://img.shields.io/badge/HTMX-1.9.10-blueviolet.svg)](https://htmx.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue.svg)](https://docs.docker.com/compose/)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-black.svg)](https://github.com/features/actions)

## 📋 Description

**M2Bilingual** is a full-featured Learning Management System (LMS) designed for an online language school. 
The project includes a REST API, JWT authentication, a student/teacher dashboard with HTMX, online tests, homework checking, and Dockerized deployment.

**Live Demo:**
- 🌐 **Website:** http://51.250.20.108/
- 🎓 **Home:** http://51.250.20.108/
- 📝 **Contact Form:** http://51.250.20.108/contact/
- 🧑‍🏫 **Teacher Cabinet:** http://51.250.20.108/teacher/
- 🧑‍🎓 **Student Cabinet:** http://51.250.20.108/student/
- 🔐 **Staff Dashboard:** http://51.250.20.108/dashboard/login/
- ⚙️ **Django Admin:** http://51.250.20.108/admin/
- 📚 **API Swagger:** http://51.250.20.108/api/docs/swagger/
- 📖 **API ReDoc:** http://51.250.20.108/api/docs/redoc/

---

## 🚀 Core Features

### 👤 Users & Auth
- ✅ Custom User model with email authentication (no username).
- ✅ JWT Authentication (access + refresh tokens).
- ✅ Roles: Student (`is_student`), Teacher (`is_teacher`), Staff, Admin.
- ✅ Role-based HTML authentication (`/login/`, `/logout/`) with automatic redirects.
- ✅ Access control decorators: `student_required`, `teacher_required`.

### 📚 Courses & Lessons
- ✅ Full CRUD for courses and lessons.
- ✅ Course pricing and publication status (`is_published`).
- ✅ YouTube video validation and automatic embed conversion.
- ✅ Lesson attachments: Video, Lecture Notes (PDF), Workbook (PDF).
- ✅ Lesson ordering.

### 🧑‍🏫 Teacher Cabinet (`/teacher/`)
- ✅ Dashboard with course and student statistics.
- ✅ Create courses and lessons.
- ✅ Lesson preview mode (👁 see the lesson exactly as a student sees it).
- ✅ **Online Test Builder:** Create single-choice, multiple-choice, text, and file-upload questions.
- ✅ **Submissions List:** View and grade student work.
- ✅ **Manual Grading:** Assign points for each question, add comments, and set the final score.
- ✅ **Progress Management:** Toggle lesson completion status for each student.
- ✅ HTMX for inline lesson editing and deletion (no page reloads).

### 🧑‍🎓 Student Cabinet (`/student/`)
- ✅ Dashboard with subscribed courses and overall progress.
- ✅ Course detail view with a list of lessons.
- ✅ Lesson view: Video player, PDF downloads, and workbook submission.
- ✅ **Online Tests:** Take tests with various question types (radio, checkbox, text, file).
- ✅ **Results:** View status, teacher's comments, and final score after checking.
- ✅ Public course preview page (`/courses/<id>/`) before purchase.

### 💳 Payments (Stripe)
- ✅ Create Stripe products and prices.
- ✅ Checkout sessions for course payments.
- ✅ Payment status tracking.

### 📨 Contact Form
- ✅ Separate page `/contact/`.
- ✅ Email notifications (Gmail SMTP) and VK messages.
- ✅ Saves to DB (`ContactRequest`).
- ✅ Honeypot spam protection.

### ⚡ Background Tasks (Celery)
- ✅ Asynchronous email notifications.
- ✅ Periodic blocking of inactive users.
- ✅ Celery Beat for scheduling.

### 🐳 DevOps
- ✅ Docker Compose (6 services).
- ✅ Nginx reverse proxy.
- ✅ CI/CD via GitHub Actions (lint → test → build → deploy).
- ✅ Automated deployment to VPS.

### 📖 Documentation
- ✅ Swagger UI (OpenAPI 3.0).
- ✅ ReDoc.
- ✅ Full endpoint descriptions.

---

## 🛠 Tech Stack

| Component | Technology | Version |
|-----------|-----------|--------|
| **Backend** | Django | 6.0.8 |
| **API** | Django REST Framework | 3.18.0 |
| **Auth** | SimpleJWT | 5.5.1 |
| **Frontend** | HTMX + Bootstrap 5 | 1.9.10 |
| **Docs** | drf-spectacular | 0.30.0 |
| **Payments** | Stripe | 15.5.0 |
| **Tasks** | Celery + Redis | 5.6.3 / 8.1.0 |
| **Database** | PostgreSQL | 15 |
| **Web Server** | Nginx | Alpine |
| **Container** | Docker Compose | 3.8+ |
| **CI/CD** | GitHub Actions | — |
| **OS** | Ubuntu | 24.04 LTS |

---

## 📦 Installation & Setup

### Requirements
- Python 3.12+
- Docker Desktop
- Git

### 1. Clone the repository
```bash
git clone https://github.com/yuliyaBarashka/Djangodrf.git
cd Djangodrf
```

### 2. Create .env

#### Copy .env.sample and fill in your credentials.

### 3. Run with Docker Compose

```bash
docker compose up -d --build 
```

#### All 6 services should be started:

- db — PostgreSQL  
- redis — Redis  
- app — Django + Gunicorn  
- celery — Celery Worker  
- celerybeat — Celery Beat  
- nginx — Reverse proxy  

### 4. Check containers

```bash
docker compose ps
```
#### All 6 containers should be Up.

### 5. Create a superuser

```bash
docker compose exec app python manage.py createsuperuser
```

#### Fill:

- Email: admin@example.com
- Password: (your) min 8 item

### 6. Open in browser

- Website: http://localhost/
- Admin: http://localhost/admin/
- Dashboard: http://localhost/dashboard/login/
- API: http://localhost/api/
- Swagger: http://localhost/api/docs/swagger/

### 🧪 Test Users
| Role | Email | Password |
|------|-------|----------|
| Teacher | `teacher@m2bilingual.ru` | `Teacher2026!` |
| Student | `student@m2bilingual.ru` | `Student2026!` |
| Superuser | `zohn12333@gmail.com` | `Admin2026Strong!` |

---

## 🌐 URL Routes

### Public Pages
| URL | Description |
|-----|-------------|
| `/` | Home page |
| `/contact/` | Contact form |
| `/privacy/` | Privacy Policy |
| `/consent/` | Data Processing Consent |
| `/kids/` | M2Bilingual Kids (landing) |
| `/courses/<id>/` | Public course preview (before purchase) |

### Authentication
| URL | Description |
|-----|-------------|
| `/login/` | Login |
| `/logout/` | Logout |

### Student Cabinet
| URL | Description |
|-----|-------------|
| `/student/` | Student dashboard |
| `/student/course/<id>/` | Course details |
| `/student/lesson/<id>/` | Lesson page (video/PDF) |
| `/student/lesson/<id>/test/` | Online test form |
| `/student/profile/` | Student profile |

### Teacher Cabinet
| URL | Description |
|-----|-------------|
| `/teacher/` | Teacher dashboard |
| `/teacher/course/<id>/` | Course management |
| `/teacher/course/create/` | Create course |
| `/teacher/course/<id>/lesson/create/` | Create lesson |
| `/teacher/lesson/<id>/questions/` | Test questions list |
| `/teacher/submissions/` | Submissions list (grading) |
| `/teacher/students/` | Students list |

---

## 🎯 API Endpoints

### Authentication
| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| POST | `/api/register/` | Register | All |
| POST | `/api/token/` | Get JWT | All |
| POST | `/api/token/refresh/` | Refresh JWT | All |

### Users
| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| GET | `/api/users/` | List | Admin |
| GET | `/api/users/{id}/` | Profile | Auth |
| PUT/PATCH | `/api/users/{id}/` | Update | Owner |
| DELETE | `/api/users/{id}/` | Delete | Owner |

### Courses & Lessons
| Method | URL | Description | Access |
|--------|-----|-------------|--------|
| GET | `/api/courses/` | List courses | Auth |
| POST | `/api/courses/` | Create course | Not Moderator |
| GET/PUT/PATCH/DELETE | `/api/courses/{id}/` | CRUD | Owner |
| GET | `/api/lessons/` | List lessons | Auth |
| POST | `/api/lessons/create/` | Create lesson | Not Moderator |
| GET/PUT/PATCH/DELETE | `/api/lessons/{id}/` | CRUD | Owner |

### Subscriptions & Payments
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/subscriptions/` | Subscribe/Unsubscribe |
| POST | `/api/payments/create/` | Create payment (Stripe) |
| GET | `/api/payments/status/` | Payment status |
| GET | `/api/payments/` | List payments |

---

## 🧪 Testing

```bash
# Run all tests
docker compose exec app python manage.py test

# Run with coverage
docker compose exec app coverage run --source='.' manage.py test
docker compose exec app coverage report
docker compose exec app coverage html
```

## 🐳 Docker Commands

```bash
# Start
docker compose up -d

# Rebuild
docker compose up -d --build

# Stop
docker compose down

# Logs
docker compose logs --tail=50 app

# Shell
docker compose exec app bash

# Django shell
docker compose exec app python manage.py shell
```

## 🚀 CI/CD

### GitHub Actions

On every push to `main`, the following workflow runs:
1. 🔍 **Lint** — flake8 checks
2. 🧪 **Test** — tests with PostgreSQL + Redis
3. 🐳 **Build** — Docker image build
4. 🚀 **Deploy** — automated deployment to VPS

### Secrets in GitHub

```env
SSH_HOST=
SSH_USER=deploy
SSH_KEY=Private SSH key
SSH_PORT=22
DEPLOY_DIR=
DJANGO_SECRET_KEY=
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
```

## 🖥 VPS Deployment

### Requirements

- Ubuntu 24.04 LTS
- Docker + Docker Compose
- SSH access
- PostgreSQL, Redis (running in Docker)

## 📁 Project Structure

```text
Djangodrf/
├── .github/
│   └── workflows/ci.yml
├── config/                 # Django settings
│   ├── celery.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                   # Landing + Contact form
│   ├── models.py           # ContactRequest
│   ├── views.py            # index, contact, privacy, consent, kids
│   └── urls.py
├── dashboard/              # Staff dashboard
│   ├── views.py
│   └── urls.py
├── lms/                    # Courses, Lessons, Tests
│   ├── models.py           # Course, Lesson, TestQuestion, TestAnswer, StudentAnswer
│   ├── views_student.py    # 🆕 Student cabinet views
│   ├── views_teacher.py    # 🆕 Teacher cabinet views
│   ├── urls_cabinet.py     # 🆕 /student/, /teacher/
│   ├── validators.py       # YouTube validation
│   ├── services.py         # Stripe
│   ├── tasks.py            # Celery
│   └── admin.py            # 🆕 Admin configuration
├── users/                  # Users, Payments, Progress
│   ├── models.py           # User, Payment, LessonProgress, CourseProgress, Submission
│   ├── decorators.py       # 🆕 student_required, teacher_required
│   ├── views.py            # 🆕 login_view, logout_view
│   ├── urls_auth.py        # 🆕 /login/, /logout/
│   └── admin.py            # 🆕 User admin with roles
├── templates/
│   ├── core/               # index, contact, privacy, kids
│   ├── users/              # login.html
│   └── lms/
│       ├── student/        # 🆕 Student templates (dashboard, course, test)
│       └── teacher/        # 🆕 Teacher templates (dashboard, questions, grading)
├── static/                 # CSS, JS, Images
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── manage.py
├── requirements.txt
└── README.md
```

## 👨‍💻 Author

Iuliia Tikhonova

- GitHub: @yuliyaBarashka
- Email: zohn12333@gmail.com











