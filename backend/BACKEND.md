# Backend API Documentation

## Структура проекта

```
backend/
├── app/
│   ├── __init__.py
│   ├── admin_config.py          # Конфигурация админ-панели
│   ├── database.py              # Подключение к БД (SQLAlchemy)
│   ├── main.py                  # Точка входа приложения
│   │
│   ├── routers/                 # API маршруты
│   │   ├── __init__.py
│   │   ├── public.py            # Публичные маршруты (главная, API)
│   │   └── admin.py             # Админ-маршруты (управление контентом)
│   │
│   ├── services/                # Бизнес-логика
│   │   ├── __init__.py
│   │   └── elements.py          # Сервис для работы с элементами
│   │
│   ├── repositories/            # Доступ к БД (SQL запросы)
│   │   ├── __init__.py
│   │   └── elements.py          # Репозиторий элементов
│   │
│   └── utils/                   # Вспомогательные функции
│       ├── __init__.py
│       └── files.py             # Кодирование изображений
│
├── migrate.py                   # Миграции БД
└── __init__.py
```

## Архитектура

### Слои приложения

1. **main.py** — точка входа
   - Инициализирует FastAPI приложение
   - Монтирует статические файлы (`/static`)
   - Регистрирует маршруты через routers

2. **routers/** — слой маршрутов
   - `public.py` — публичные маршруты (для общего доступа)
   - `admin.py` — административные маршруты (управление контентом)

3. **services/** — бизнес-логика
   - Обработка бизнес-правил
   - Валидация данных
   - Координация между repositories и routers

4. **repositories/** — доступ к данным
   - SQL запросы
   - Работа с БД
   - Возвращение чистых данных

5. **utils/** — вспомогательные функции
   - Обработка файлов
   - Кодирование данных

## Структура БД

### Основные таблицы

- **sections** — разделы сайта (hero, team, timeline, etc.)
- **elements** — элементы контента в разделах
- **element_types** — типы элементов (stat, card, text, etc.)

### Связи

- Element → Section (многие-к-одному)
- Element → ElementType (многие-к-одному)

---

## API Маршруты

### Публичные маршруты (`routers/public.py`)

#### 1. GET `/`
**Главная страница**

Возвращает HTML главную страницу со всем контентом.

**Ответ:**
- 200: HTML страница с контентом
- Шаблон: `frontend/templates/index.html`

**Контекст передачи:**
```
{
  "data": {
    "hero": [...],
    "team": [...],
    "timeline": [...],
    ...
  }
}
```

#### 2. GET `/api/content`
**API для получения контента**

Возвращает JSON с контентом всех разделов.

**Ответ:** 200
```json
{
  "hero": [
    {
      "id": 1,
      "position": 1,
      "type": "stat",
      "heading": "500+",
      "text": "Сотрудников",
      "label": "достижение",
      "image": "...",
      "link": "..."
    }
  ],
  "team": [...],
  "timeline": [...]
}
```

---

### Административные маршруты (`routers/admin.py`)

#### Основной шаблон URL
```
/admin/{section_name}/{element_id}/{action}
```

где:
- `section_name` — имя раздела (hero, team, timeline, etc.)
- `element_id` — ID элемента (опционально для create)
- `action` — операция (edit, delete, create)

---

#### 1. GET `/admin`
**Список всех разделов админки**

Возвращает список разделов для управления.

**Ответ:** 200 (HTML)
- Шаблон: `frontend/templates/admin/index.html`
- Контекст:
```
{
  "sections": [
    {"name": "Hero", "slug": "hero"},
    {"name": "Team", "slug": "team"},
    ...
  ]
}
```

---

#### 2. GET `/admin/{section_name}`
**Список элементов раздела**

Показывает все элементы в конкретном разделе с возможностью редактирования/удаления.

**Параметры:**
- `section_name` (path): имя раздела (например, "hero", "team")

**Ответ:** 200 (HTML)
- Шаблон: `frontend/templates/admin/section.html`
- Контекст:
```
{
  "section_name": "hero",
  "elements": [
    {
      "id": 1,
      "type": "stat",
      "position": 1,
      "heading": "500+",
      "text": "Сотрудников",
      "...": "..."
    }
  ]
}
```

**Ошибки:**
- 404: Раздел не найден

---

#### 3. GET `/admin/{section_name}/create`
**Форма создания элемента**

Показывает форму для добавления нового элемента в раздел.

**Параметры:**
- `section_name` (path): имя раздела

**Ответ:** 200 (HTML)
- Шаблон: `frontend/templates/admin/form.html`
- Контекст:
```
{
  "mode": "create",
  "title": "Создание элемента",
  "button": "Создать",
  "section_name": "hero",
  "element": null,
  "fields": ["heading", "text", "position"],
  "types": ["stat", "card", "text"],
  "preview": "hero",
  "positions": [1, 2, 3],
  "default_position": 3
}
```

**Ошибки:**
- 404: Раздел не найден

---

#### 4. POST `/admin/{section_name}/create`
**Создать новый элемент**

Сохраняет новый элемент в разделе.

**Параметры (form-data):**
- `element_type` (строка): тип элемента (stat, card, text и т.д.)
- `position` (число): позиция в разделе
- `heading` (опционально): заголовок
- `subtitle` (опционально): подзаголовок
- `text` (опционально): текст/описание
- `label` (опционально): метка/тег
- `link` (опционально): ссылка
- `image` (опционально): загруженное изображение

**Ответ:**
- 303: Редирект на `/admin/{section_name}` (успех)
- 400: Ошибка валидации или недопустимый тип
- 404: Раздел не найден

**Логика:**
1. Проверка конфигурации раздела
2. Валидация типа элемента
3. Кодирование изображения в base64 (если загружено)
4. Фильтрация полей через ADMIN_CONFIG
5. Сдвиг позиций существующих элементов
6. Вставка нового элемента в БД

---

#### 5. GET `/admin/{section_name}/{element_id}/edit`
**Форма редактирования элемента**

Показывает форму с текущими данными элемента для редактирования.

**Параметры:**
- `section_name` (path): имя раздела
- `element_id` (path): ID элемента

**Ответ:** 200 (HTML)
- Шаблон: `frontend/templates/admin/form.html`
- Контекст:
```
{
  "mode": "edit",
  "title": "Редактирование элемента",
  "button": "Сохранить",
  "section_name": "hero",
  "element": {
    "element_id": 1,
    "position": 1,
    "heading": "500+",
    "type": "stat",
    ...
  },
  "fields": [...],
  "types": [...],
  "positions": [1, 2, 3],
  "default_position": 1
}
```

**Ошибки:**
- 404: Раздел или элемент не найден

---

#### 6. POST `/admin/{section_name}/{element_id}/edit`
**Обновить элемент**

Сохраняет изменения элемента.

**Параметры (form-data):**
- Те же, что и при создании
- `element_type`: новый тип
- `position`: новая позиция
- `heading`, `subtitle`, `text`, `label`, `link` (опционально)
- `image` (опционально): новое изображение

**Ответ:**
- 303: Редирект на `/admin/{section_name}` (успех)
- 400: Ошибка валидации
- 404: Раздел или элемент не найден

**Логика:**
1. Получение старых данных элемента
2. Сохранение значений, если новые не предоставлены
3. Если позиция изменилась — обмен позициями с другим элементом
4. Обновление записи в БД

---

#### 7. POST `/admin/{section_name}/{element_id}/delete`
**Удалить элемент**

Удаляет элемент и пересчитывает позиции остальных.

**Параметры:**
- `section_name` (path): имя раздела
- `element_id` (path): ID элемента

**Ответ:**
- 303: Редирект на `/admin/{section_name}` (успех)
- 404: Раздел или элемент не найден

**Логика:**
1. Получение информации об элементе (section_id, position)
2. Удаление элемента
3. Сдвиг всех элементов после удаленного вверх по позиции

---

## Конфигурация разделов (`admin_config.py`)

Определяет поведение и доступные поля для каждого раздела:

```python
ADMIN_CONFIG = {
    "section_name": {
        "fields": ["heading", "text", "image", "link"],  # Доступные поля
        "types": ["stat", "card", "text"],               # Доступные типы
        "preview": "card"                                # Тип предпросмотра
    }
}
```

---

## Сервисный слой (`services/elements.py`)

### Функции

#### `create_element_service()`
Создание нового элемента с валидацией.

**Параметры:**
- `section_name`, `element_type`, `position`
- `heading`, `subtitle`, `text_value`, `label`, `link`
- `image` (UploadFile), `config` (dict)

**Возвращает:**
- (True, "message") — успех
- (None, "error") — ошибка

**Процесс:**
1. Кодирование изображения
2. Фильтрация полей через конфиг
3. Валидация позиции
4. Сдвиг позиций и вставка

---

#### `update_element_service()`
Обновление существующего элемента.

**Параметры:** аналогично create, но с добавлением `element_id`

**Возвращает:** (True/None, "message")

**Процесс:**
1. Получение старых данных
2. Заполнение пустых полей старыми значениями
3. Обмен позициями при необходимости
4. Обновление записи

---

#### `delete_element_service()`
Удаление элемента.

**Параметры:**
- `section_name`, `element_id`

**Возвращает:** (True/None, "message")

**Процесс:**
1. Получение раздела и позиции
2. Удаление из БД
3. Пересчёт позиций

---

## Уровень репозитория (`repositories/elements.py`)

Содержит все SQL запросы для работы с элементами.

### Основные функции

- `get_elements_by_section(section_name)` — получить все элементы раздела
- `get_element_by_id(element_id, section_name)` — получить один элемент
- `get_max_position_in_section(section_name)` — макс позиция в разделе
- `get_content_by_sections()` — контент всех разделов (для главной)
- `create_element(...)` — вставить новый элемент
- `update_element(...)` — обновить элемент
- `delete_element(element_id, connection)` — удалить элемент
- `shift_positions_up/down()` — пересчёт позиций

---

## Обработка файлов (`utils/files.py`)

### `encode_image_to_base64(image: UploadFile)`

Кодирует загруженное изображение в data URI (base64).

**Возвращает:**
```
data:image/png;base64,iVBORw0KGgoAAAANS...
```

**Процесс:**
1. Чтение содержимого файла
2. Кодирование в base64
3. Оформление как data URI

---

## Примеры запросов

### Получить контент (публичный API)
```bash
curl http://localhost:8000/api/content
```

### Создать элемент
```bash
curl -X POST http://localhost:8000/admin/hero/create \
  -F "element_type=stat" \
  -F "position=1" \
  -F "heading=500+" \
  -F "text=Сотрудников" \
  -F "image=@image.png"
```

### Редактировать элемент
```bash
curl -X POST http://localhost:8000/admin/hero/1/edit \
  -F "element_type=stat" \
  -F "position=2" \
  -F "heading=1000+"
```

### Удалить элемент
```bash
curl -X POST http://localhost:8000/admin/hero/1/delete
```

---

## Установка и запуск

### Требования
- Python 3.9+
- PostgreSQL
- FastAPI
- SQLAlchemy

### Установка зависимостей
```bash
pip install -r requirements.txt
```

### Миграции
```bash
python backend/migrate.py
```

### Запуск
```bash
uvicorn backend.app.main:app --reload
```

Приложение будет доступно на `http://localhost:8000`

---

## Поле конфигурации ADMIN_CONFIG

Каждый раздел в `admin_config.py` имеет структуру:

```python
{
    "fields": [],      # Список доступных полей
    "types": [],       # Список типов элементов
    "preview": ""      # Тип предпросмотра (hero, card, stat, text)
}
```

**Доступные поля:**
- `heading` — заголовок
- `subtitle` — подзаголовок
- `text` — основной текст
- `label` — метка/тег
- `link` — ссылка
- `image` — изображение

**Доступные типы:** определяются в таблице `element_types` БД

**Типы предпросмотра:**
- `hero` — полноэкранный баннер
- `card` — карточка с изображением
- `stat` — статистика (число + текст)
- `text` — просто текст

---

## Обработка ошибок

Все ошибки возвращаются с соответствующими HTTP статусами:

| Статус | Значение | Пример |
|--------|----------|--------|
| 200 | OK | Успешно получены данные |
| 303 | Redirect | Успешно создано/обновлено/удалено |
| 400 | Bad Request | Неверные параметры, недопустимый тип |
| 404 | Not Found | Раздел/элемент не найден |

---

## Безопасность

- ✅ Валидация типов через ADMIN_CONFIG
- ✅ Проверка существования элементов
- ✅ Экранирование SQL параметров (SQLAlchemy)
- ✅ Base64 кодирование изображений вместо загрузки на диск

---

## Цепочка запроса

```
HTTP запрос
    ↓
router (public.py / admin.py)
    ↓
service (elements.py) — бизнес-логика
    ↓
repository (elements.py) — SQL запросы
    ↓
database (SQLAlchemy/PostgreSQL)
    ↓
response
```

---

