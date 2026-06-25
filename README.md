# travelline_project
репозиторий для проекта travelline. Реализация конструктора сайтов на базе https://travelline.tech/
# TravelLine Tech CMS

Учебный проект по разработке веб-приложения с управляемым контентом.

## Описание

Приложение состоит из двух частей:

1. **Публичная часть** — главная страница портала TravelLine Tech.
2. **Административная панель** — интерфейс для управления содержимым публичной страницы.

Администратор может:

* изменять тексты блоков;
* добавлять новые блоки;
* удалять существующие блоки;
* изменять порядок отображения блоков.

Все изменения сохраняются в базе данных и отображаются на публичной странице без перезапуска сервера.

---

# Технологический стек

## Backend

* Python 3.13+
* FastAPI
* SQLAlchemy 2.0
* Alembic
* Pydantic
* JWT Authentication

## Frontend

* Jinja2
* HTMX
* Bootstrap 5
* Vanilla JavaScript

## Database

* PostgreSQL

## Infrastructure

* Docker
* Docker Compose

---

# Архитектура

Проект реализован в виде монолитного веб-приложения.

```text
┌─────────────────────┐
│      Browser        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│      FastAPI        │
├─────────────────────┤
│ Public Routes       │
│ Admin Routes        │
│ Auth Routes         │
│ Business Logic      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     PostgreSQL      │
└─────────────────────┘
```

---

# Основные компоненты

## Public Module

Отвечает за отображение публичной страницы сайта.

Функции:

* получение контента из БД;
* отображение блоков;
* отображение изменений без перезапуска приложения.

## Admin Module

Отвечает за управление контентом.

Функции:

* создание блоков;
* редактирование блоков;
* удаление блоков;
* изменение порядка блоков.

## Authentication Module

Отвечает за авторизацию администратора.

Функции:

* вход в систему;
* проверка JWT токена;
* защита административных маршрутов.

## Persistence Layer

Слой работы с данными.

Используемые инструменты:

* PostgreSQL;
* SQLAlchemy;
* Alembic.

---

# Предварительная структура проекта

```text
project/

├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── auth.py
│   ├── routes/
│   │   ├── public.py
│   │   ├── admin.py
│   │   └── auth.py
│   └── services/
│
├── templates/
│   ├── index.html
│   ├── admin.html
│   └── login.html
│
├── static/
│   ├── css/
│   └── js/
│
├── migrations/
│
├── docker-compose.yml
│
├── Dockerfile
│
├── requirements.txt
│
└── README.md
```

 # Динамическая структура страницы

 ```text
 Header
│
├── Hero
│
├── Statistics
│
├── Team
│
├── Timeline
│
├── Directions
│
├── Vacancies
│
├── Offices
│
├── Benefits
│
├── Contact Form
│
└── Footer

--- Щас работаем над:

Header
├── logo
└── menu[]

Hero
├── title
├── subtitle
├── description
├── button
└── image

Statistics
├── value
└── label

Team
├── name
├── position
├── description
└── photo
 ```