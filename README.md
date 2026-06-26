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

# Общая структура таблиц:

```text
page
 │
 └──── section
          │
          └──── element
                    │
                    └──── element_type

role
 │
 └──── user
```

 # Миграции:

 ```text
 migrations/
│
├── 001_create_users.py
├── 002_create_content.py
└── 003_seed_initial_data.py
 ```

### 001_create_users.py
Создает только структуру.

```text
role
----
role_id
name

user
----
user_id
role_id
name
login
password_hash
```

### 002_create_content.py
Создает только

```text
pages
----
page_id
title


sections
-------
section_id
page_id
name


element_type
------------
type_id
name


elements
-------
element_id
section_id
type_id
position
heading
text
image
link
```

### 003_seed_initial_data.py

Наполняем роли и юзеров

### 004_seed_site_content.py

Создаем записи в таблице sections

Header
Hero
Statistics
Team
Timeline
Directions
Vacancies
Offices
Benefits
Contact
Footer

Затем наполняет таблицу elements.

| section_id | position | heading | text            | type   | link       |
| ---------- | -------- | ------- | --------------- | ------ | ---------- |
| 1          | 1        | NULL    | TravelLine Tech | text   | NULL       |
| 1          | 2        | NULL    | Команда         | button | #team      |
| 1          | 3        | NULL    | Вакансии        | button | #vacancies |
| 1          | 4        | NULL    | Контакты        | button | #contact   |

И тд....

# Итоговый seed базы данных.

Получится цепочка миграций:

001_create_users_roles.py
    ↓
Создает таблицы roles и users

002_create_sections_elements.py
    ↓
Создает таблицы sections и elements

003_seed_users_roles.py
    ↓
Заполняет роли и тестовых пользователей

004_seed_site_content.py
    ↓
Создает все секции сайта
    и заполняет их начальными элементами