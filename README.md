# TravelLine Tech — Динамический конструктор сайтов

Веб-приложение для управления контентом портала **TravelLine Tech**. Реализует полноценный CMS с публичной страницей и административной панелью.

**Репозиторий:** https://github.com/travelline/tech  
**Демо:** https://travelline.tech/

---

## 📋 Описание

TravelLine Tech CMS — это многоязычный конструктор коммерческих веб-сайтов. Позволяет администраторам управлять контентом (текст, изображения, ссылки) через интуитивный интерфейс без знания HTML/CSS.

### Основные возможности

✅ **Публичная часть** — красивая главная страница с 13 секциями  
✅ **Админ-панель** — управление всем контентом через веб-интерфейс  
✅ **Реал-тайм preview** — коннотация при редактировании элементов  
✅ **Динамический контент** — все изменения сохраняются в БД  
✅ **Адаптивный дизайн** — работает на всех устройствах (Bootstrap 5)  
✅ **Быстрая обработка** — асинхронный FastAPI  

---

## 🛠️ Технологический стек

### Backend
- **Framework:** FastAPI (Python 3.9+)
- **Database:** PostgreSQL + SQLAlchemy ORM
- **Architecture:** Clean Layered Architecture (Routers → Services → Repositories)
- **Templating:** Jinja2
- **Validation:** Pydantic

### Frontend
- **Templating:** Jinja2
- **CSS Framework:** Bootstrap 5.3.3 (CDN)
- **JavaScript:** Vanilla JS (admin-form.js)
- **Responsive:** Mobile-first approach

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Servers:** Uvicorn (FastAPI ASGI)

---

## 📁 Структура проекта

```
travelline_project/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI приложение (точка входа)
│   │   ├── database.py             # SQLAlchemy конфигурация
│   │   ├── admin_config.py         # Конфиг админ-панели (поля, типы)
│   │   │
│   │   ├── routers/                # HTTP маршруты
│   │   │   ├── __init__.py
│   │   │   ├── public.py           # Публичные endpoints (GET /, GET /api/content)
│   │   │   └── admin.py            # Админ endpoints (CRUD элементов)
│   │   │
│   │   ├── services/               # Бизнес-логика
│   │   │   ├── __init__.py
│   │   │   └── elements.py         # Сервисы CRUD элементов
│   │   │
│   │   ├── repositories/           # Работа с БД
│   │   │   ├── __init__.py
│   │   │   └── elements.py         # SQL запросы для элементов
│   │   │
│   │   └── utils/                  # Вспомогательные функции
│   │       ├── __init__.py
│   │       └── files.py            # Работа с файлами, base64 encoding
│   │
│   ├── migrations/                 # Alembic DB миграции
│   │   ├── 001_create_users_roles.py
│   │   ├── 002_create_sections_elements.py
│   │   ├── 003_seed_users_roles.py
│   │   └── 004_seed_site_content.py
│   │
│   ├── __init__.py
│   └── migrate.py                  # Скрипт запуска миграций
│
├── frontend/
│   ├── templates/                  # Jinja2 шаблоны
│   │   ├── index.html              # Главная страница (13 секций)
│   │   └── admin/
│   │       ├── index.html          # Список разделов админки
│   │       ├── section.html        # Список элементов в разделе
│   │       └── form.html           # Форма создания/редактирования
│   │
│   └── static/                     # Статические файлы
│       ├── css/
│       │   ├── styleHome.css       # Стили главной страницы
│       │   └── styleForm.css       # Стили админ-панели
│       └── js/
│           └── admin-form.js       # Реал-тайм preview в форме
│
├── json/                           # JSON примеры
│   └── struct_json.json
│  
│
├── Dockerfile                      # Конфигурация Docker
├── docker-compose.yml              # Оркестрация контейнеров
├── requirements.txt                # Python зависимости
│
├── BACKEND.md                      # Документация backend
├── FRONTEND.md                     # Документация frontend
├── README.md                       # Этот файл
└── ERROR.md / ADMIN.md / ...      # Дополнительные заметки
```

---

## 🏗️ Архитектура

### Слоистая архитектура (Clean Architecture)

```
┌─────────────────────────────────────┐
│         HTTP Requests               │
│      (Browser / Admin Client)       │
└────────────────┬────────────────────┘
                 │
┌─────────────────▼────────────────────┐
│       ROUTERS (routers/*.py)         │
│  - public.py (2 endpoints)           │
│  - admin.py (7 endpoints)            │
└────────────────┬────────────────────┘
                 │
┌─────────────────▼────────────────────┐
│      SERVICES (services/*.py)        │
│  - Business logic                    │
│  - Validation                        │
│  - Error handling                    │
└────────────────┬────────────────────┘
                 │
┌─────────────────▼────────────────────┐
│    REPOSITORIES (repositories/*.py)  │
│  - SQL queries                       │
│  - Data access                       │
│  - ORM operations                    │
└────────────────┬────────────────────┘
                 │
┌─────────────────▼────────────────────┐
│    DATABASE (PostgreSQL)             │
│  - Tables, schemas, indexes          │
└──────────────────────────────────────┘
```

**Преимущества:**
- 🔄 Слабая связанность — легко тестировать и модифицировать
- 🔌 Pluggable — можно менять НИЖние слои без изменения выше
- 📚 Понятная структура — каждая папка имеет одну обязанность
- 🚀 Масштабируемость — просто добавить новые роутеры/сервисы

---

## 🌐 Секции главной страницы

```
index.html содержит 13 динамических секций:

1. Header        — Фиксированная навигация с логотипом
2. Hero          — Главный баннер (заголовок + статистика)
3. Statistics    — Цифры о компании
4. Team          — Команда (карточки сотрудников)
5. Timeline      — История развития
6. Clients       — Наши клиенты
7. Directions    — Направления разработки
8. Vacancies     — Открытые вакансии
9. Gallery       — Галерея проектов
10. Offices      — Наши офисы
11. Benefits     — Преимущества работы
12. Contact      — Форма обратной связи
13. Footer       — Подвал с ссылками
```

Все секции рендерятся из БД через Jinja2.

---

## 🔌 API Endpoints

### Публичные (без авторизации)

| Метод | Endpoint | Описание |
|-------|----------|---------|
| GET | `/` | Главная страница (HTML) |
| GET | `/api/content` | Весь контент (JSON) |

### Административные (требуется авторизация)

| Метод | Endpoint | Описание |
|-------|----------|---------|
| GET | `/admin` | Список всех разделов |
| GET | `/admin/{section}` | Список элементов в разделе |
| GET | `/admin/{section}/create` | Форма создания элемента |
| POST | `/admin/{section}/create` | Создание элемента |
| GET | `/admin/{section}/{id}/edit` | Форма редактирования |
| POST | `/admin/{section}/{id}/edit` | Сохранение изменений |
| POST | `/admin/{section}/{id}/delete` | Удаление элемента |

**Подробно:** см. [BACKEND.md](BACKEND.md)

---

## 🚀 Быстрый старт

### 1. Требования

- Docker + Docker Compose (рекомендуется)
- ИЛИ PostgreSQL + Python 3.9+

### 2. Установка

#### Через Docker (рекомендуется)

```bash
git clone https://github.com/travelline/tech.git
cd travelline_project

docker-compose up -d
```

Приложение будет доступно на `http://localhost:8000`

#### Локально (без Docker)

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Настроить .env файл
cp .env.example .env
# Отредактировать DATABASE_URL=postgresql://user:pass@localhost:5432/travelline

# 3. Запустить миграции
python backend/migrate.py

# 4. Запустить сервер
uvicorn backend.app.main:app --reload
```

Приложение будет доступна на `http://localhost:8000`

---

## 🗄️ База данных

### Структура таблиц

#### Таблица `users`
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'user'
);
```

#### Таблица `site_sections`
```sql
CREATE TABLE site_sections (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    display_name VARCHAR(255)
);
```

#### Таблица `site_elements`
```sql
CREATE TABLE site_elements (
    id SERIAL PRIMARY KEY,
    section_id INTEGER REFERENCES site_sections(id),
    element_type VARCHAR(50),
    position INTEGER,
    heading TEXT,
    subheading TEXT,
    text LONGTEXT,
    label TEXT,
    image LONGTEXT,  -- base64 encoded
    link TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Миграции

```bash
# Посмотреть список миграций
ls backend/migrations/

# Запустить все миграции
python backend/migrate.py

# Откатить последнюю миграцию
# (Требует Alembic downgrade)
```

---

## 📝 Логирование и отладка

### Просмотр логов (Docker)

```bash
docker-compose logs -f app
```

### Путь к логам (локально)

`/var/log/travelline/ directory`

---

## 🧪 Тестирование

### Запуск тестов (если есть)

```bash
pytest backend/tests/
```

### Проверка синтаксиса Python

```bash
python -m py_compile backend/app/*.py backend/app/**/*.py
```

---

## 📚 Документация

- **[BACKEND.md](BACKEND.md)** — Полная документация backend (архитектура, endpoints, примеры)
- **[FRONTEND.md](FRONTEND.md)** — Полная документация frontend (шаблоны, компоненты, стили)
- **[API Specification](openapi.yaml)** — OpenAPI/Swagger спецификация

Просмотреть интерактивную документацию API:
```
http://localhost:8000/docs → Swagger UI
http://localhost:8000/redoc → ReDoc
```

---

## 🔐 Безопасность

- ✅ CORS настроены для локального окружения
- ✅ JWT токены для админ-панели (если включена авторизация)
- ✅ SQL injection защита через SQLAlchemy ORM
- ✅ CSRF защита на формах (Jinja2 templates)

**Важно:** В production обновить:
- `SECRET_KEY` в конфигурации
- CORS origins
- Database credentials
- SSL/TLS на nginx proxy

---

## 🐛 Решение проблем

### "Connection refused" при запуске

**Проблема:** Приложение не может подключиться к БД

**Решение:**
```bash
# Проверить, запущена ли БД
docker ps

# Если БД не запущена
docker-compose up -d postgres
```

### "Port already in use"

**Проблема:** Порт 8000 уже занят

**Решение:**
```bash
# Найти процесс
lsof -i :8000

# Или использовать другой порт
uvicorn backend.app.main:app --port 8001
```

### Шаблон не рендерится

**Проблема:** Ошибка в Jinja2 синтаксисе

**Решение:**
- Проверить скобки: `{{ }}` для переменных, `{% %}` для логики
- Проверить indentation (должно быть 2 пробела)
- Смотреть логи: `docker-compose logs app`

---

## 📈 Масштабирование

### Добавление нового раздела

1. Добавить в `admin_config.py`:
```python
ADMIN_CONFIG = {
    "my_section": {
        "fields": ["heading", "text", "image"],
        "types": ["card", "text"],
        "preview": "card"
    }
}
```

2. Добавить в `index.html`:
```html
<section id="my_section">
  {% for item in data.my_section %}
    <!-- Рендер -->
  {% endfor %}
</section>
```

3. Добавить в БД через админ-панель

**Подробно:** см. [FRONTEND.md](FRONTEND.md#добавление-нового-раздела)

---

## 📦 Зависимости

### Backend
```
fastapi==0.104.1
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
jinja2==3.1.2
pydantic==2.5.0
uvicorn==0.24.0
```

### Frontend
```
Bootstrap 5.3.3 (CDN)
Vanilla JavaScript (no dependencies)
```

Полный список: [requirements.txt](requirements.txt)

---

## 🤝 Контрибьютинг

1. Создать ветку: `git checkout -b feature/my-feature`
2. Сделать коммиты: `git commit -am 'Add feature'`
3. Запушить: `git push origin feature/my-feature`
4. Открыть Pull Request

---

## 📖 Дополнительные ресурсы

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Jinja2 Templates](https://jinja.palletsprojects.com/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 📄 Лицензия

MIT License — см. [LICENSE](LICENSE)

---

## 👨‍💼 Разработчик

**TravelLine Tech Team**

Версия: 2.0 (refactored с чистой архитектурой)  
Дата обновления: 1 июля 2026
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