# Frontend Documentation

## Структура проекта

```
frontend/
├── templates/               # HTML шаблоны (Jinja2)
│   ├── index.html          # Главная страница сайта
│   │
│   └── admin/              # Административная панель
│       ├── index.html      # Список разделов админки
│       ├── section.html    # Список элементов в разделе
│       └── form.html       # Форма создания/редактирования элемента
│
├── static/                 # Статические файлы
│   ├── css/
│   │   ├── styleHome.css   # Стили главной страницы
│   │   └── styleForm.css   # Стили админ-панели
│   │
│   └── js/
│       └── admin-form.js   # JavaScript для админ-формы
```

---

## Архитектура

### Шаблонизация (Jinja2)

Проект использует **Jinja2** для шаблонизации. Все шаблоны находятся в папке `frontend/templates/` и рендерятся на backend через FastAPI.

**Процесс:**
1. Backend получает данные из БД
2. Передаёт их в шаблон через контекст
3. Jinja2 рендерит HTML
4. Браузер получает готовую страницу

---

## Главная страница (`index.html`)

### Структура

Главная страница динамически состоит из нескольких секций:

```
1. Header (навигация)
2. Hero (главный баннер с заголовком)
3. Statistics (статистика из БД)
4. Team (команда)
5. Timeline (история компании)
6. Clients (клиенты)
7. Directions (направления разработки)
8. Vacancies (вакансии)
9. Gallery (галерея)
10. Offices (офисы)
11. Benefits (преимущества)
12. Contact (форма обратной связи)
13. Footer
```

### Компоненты

#### Header / Navigation
```html
<nav class="navbar navbar-expand-lg fixed-top">
  <!-- Логотип -->
  <a class="navbar-brand">TRAVELLINE</a>
  
  <!-- Меню навигации -->
  <div class="navbar-nav ms-auto">
    <a href="#hero">О Travelline</a>
    <a href="#timeline">Наши инструменты</a>
    <a href="#team">Команда</a>
    <a href="#directions">Направления</a>
    <a href="#vacancies">Вакансии</a>
  </div>
</nav>
```

**Скользящая (fixed-top) навигация с якорными ссылками на разделы.**

---

#### Hero Section
```html
<section class="hero" id="hero">
  <div class="container">
    <h1>Стабильно растем и принимаем новые вызовы</h1>
  </div>
</section>
```

**Главный баннер со статистикой, загруженной через Jinja2 из БД.**

---

#### Dynamic Sections (из БД)
```html
{% for item in data.hero %}
  {% if item.type == "stat" %}
    <div class="stat-number">{{ item.heading }}</div>
    <p>{{ item.text }}</p>
  {% endif %}
{% endfor %}
```

**Все секции (team, timeline, clients, etc.) рендерятся из контекста `data`.**

---

## Административная панель

### 1. Главная админки (`admin/index.html`)

**URL:** `/admin`

**Назначение:** Показывает список всех разделов для управления

**Компоненты:**
- Кнопка "Все разделы" (ссылка назад)
- Список разделов с кликабельными ссылками

**Пример:**
```html
{% for section in sections %}
  <a href="/admin/{{ section.slug }}">
    <strong>{{ section.name }}</strong>
  </a>
{% endfor %}
```

---

### 2. Раздел админки (`admin/section.html`)

**URL:** `/admin/{section_name}`

**Назначение:** Показывает все элементы в одном разделе

**Компоненты:**
- Кнопка "Все разделы" (навигация назад)
- Заголовок раздела
- Кнопка "Добавить элемент" (ссылка на форму создания)
- Список элементов в виде карточек

**Каждый элемент показывает:**
- Тип элемента (badge)
- Позицию (badge)
- Заголовок (если есть)
- Подзаголовок (если есть)
- Текст (если есть)
- Изображение (если есть)
- Кнопки "Редактировать" и "Удалить"

**Пример:**
```html
{% for element in elements %}
  <div class="card">
    <div class="d-flex justify-content-between">
      <span class="badge">{{ element.type }}</span>
      <span>Позиция: {{ element.position }}</span>
    </div>
    
    <h5>{{ element.heading }}</h5>
    <p>{{ element.text }}</p>
    
    <div class="d-flex gap-2">
      <a href="/admin/{{ section_name }}/{{ element.id }}/edit" class="btn btn-primary">
        Редактировать
      </a>
      <form method="post" action="/admin/{{ section_name }}/{{ element.id }}/delete">
        <button type="submit" class="btn btn-danger">Удалить</button>
      </form>
    </div>
  </div>
{% endfor %}
```

**Пустое состояние:**
```html
{% if elements|length == 0 %}
  <div class="alert alert-info">
    В этом разделе пока нет элементов
  </div>
{% endif %}
```

---

### 3. Форма админки (`admin/form.html`)

**URL:** 
- GET: `/admin/{section_name}/create` или `/admin/{section_name}/{element_id}/edit`
- POST: то же

**Назначение:** Форма для создания и редактирования элементов

**Структура:**
```
┌─────────────────────────────────────┐
│         Заголовок формы             │
│       (Создание/Редактирование)     │
├─────────────────────────────────────┤
│  [Левая колонка 70%]  [Правая 30%]  │
│                                     │
│  ФОРМА:                  PREVIEW:    │
│  - Тип элемента         (динамич)   │
│  - Позиция                          │
│  - Поля (динамич):                  │
│    * Заголовок                      │
│    * Подзаголовок                   │
│    * Текст                          │
│    * Метка                          │
│    * Изображение                    │
│    * Ссылка                         │
│  [Кнопка "Создать/Сохранить"]       │
└─────────────────────────────────────┘
```

#### Динамические поля

Какие поля показываются зависит от конфига раздела (`admin_config.py`):

```jinja2
{% if "heading" in fields %}
  <div class="mb-3">
    <label>Заголовок</label>
    <input type="text" name="heading" id="heading" 
           value="{{ element.heading if element else '' }}"
           oninput="updatePreview()">
  </div>
{% endif %}

{% if "image" in fields %}
  <div class="mb-3">
    <label>Изображение</label>
    <input type="file" name="image" id="image" 
           accept="image/*" onchange="previewImage(event)">
    {% if element and element.image %}
      <img src="{{ element.image }}" style="max-width:300px;">
    {% endif %}
  </div>
{% endif %}
```

#### Предпросмотр (справа)

Показывает реал-тайм предпросмотр элемента по мере заполнения формы:

```jinja2
{% if preview == "hero" %}
  <section class="hero-preview">
    <h1 id="preview-heading">Стабильно растем</h1>
    <p id="preview-text">Описание</p>
  </section>
{% endif %}

{% if preview == "card" %}
  <div class="card">
    <img id="preview-image" class="card-img-top">
    <div class="card-body">
      <h5 id="preview-heading">Название</h5>
      <p id="preview-text">Описание</p>
    </div>
  </div>
{% endif %}

{% if preview == "stat" %}
  <div class="text-center">
    <div class="stat-number" id="preview-heading">500+</div>
    <p id="preview-text">Сотрудников</p>
  </div>
{% endif %}
```

#### Типы Предпросмотра

| Тип | Где использован | Пример |
|-----|-----------------|--------|
| `hero` | Hero секция | Большой баннер с текстом |
| `card` | Team, Clients, Gallery | Карточка с изображением |
| `stat` | Statistics | Число + метка |
| `text` | Timeline, Directions | Просто текст |

---

## Статические файлы

### CSS (`static/css/`)

#### `styleHome.css`
Стили главной страницы:
- Навигация (header, navbar)
- Секции (padding, background)
- Карточки (team, clients, gallery)
- Формы (contact)
- Адаптивность (media queries)

**Использует Bootstrap 5 классы:**
- `.container` — контейнер с максимальной шириной
- `.row` / `.col-md-*` — сетка
- `.card` — карточка
- `.badge` — значки
- `.btn` — кнопки
- `.d-flex` / `.justify-content-between` — flexbox

#### `styleForm.css`
Стили админ-панели:
- Форма (поля ввода, select)
- Preview (справа)
- Кнопки действий
- Responsive layout

---

### JavaScript (`static/js/`)

#### `admin-form.js`

Реализует интерактивность в админ-форме:

```javascript
function updatePreview() {
  const heading = document.getElementById("heading");
  const text = document.getElementById("text");
  
  // Обновляет preview-heading и preview-text в реал-тайме
  document.querySelectorAll("#preview-heading").forEach(item => {
    item.innerText = heading?.value || "Заголовок";
  });
}

function previewImage(event) {
  const image = document.getElementById("preview-image");
  const file = event.target.files[0];
  
  if (file) {
    image.src = URL.createObjectURL(file);
    image.style.display = "block";
  }
}
```

**Функции:**
- `updatePreview()` — обновляет текст в предпросмотре при изменении поля
- `previewImage(event)` — показывает выбранное изображение в предпросмотре

---

## Взаимодействие с Backend

### Директивы Jinja2

#### Переменные контекста
```jinja2
{{ variable }}              <!-- Вывод переменной -->
{{ object.property }}       <!-- Свойство объекта -->
{{ list[0] }}              <!-- Элемент списка -->
```

#### Циклы
```jinja2
{% for item in items %}
  <div>{{ item.name }}</div>
{% endfor %}
```

#### Условия
```jinja2
{% if item.image %}
  <img src="{{ item.image }}">
{% endif %}
```

#### Фильтры
```jinja2
{{ section_name|capitalize }}   <!-- "hero" → "Hero" -->
{{ item.text|truncate(100) }}   <!-- Обрезка текста -->
```

#### Проверка длины
```jinja2
{% if elements|length == 0 %}
  Нет элементов
{% endif %}
```

---

## Формы

### Главная страница (Contact)

**HTML:**
```html
<form>
  <input type="text" placeholder="Имя">
  <input type="email" placeholder="Email">
  <textarea placeholder="Сообщение"></textarea>
  {% for item in data.contact %}
    {% if item.type == "button" %}
      <button>{{ item.text }}</button>
    {% endif %}
  {% endfor %}
</form>
```

**Метод:** GET/POST (зависит от конфигурации в backend)

---

### Админ-формы

**Методы:**
- GET — показ формы
- POST — отправка данных

**Типы данных:**
```
method="post"
enctype="multipart/form-data"  <!-- Для загрузки файлов -->
```

**Поля (form-data):**
```
element_type=stat
position=1
heading=500+
text=Сотрудников
image=<binary>
```

---

## Компоненты UI

### Bootstrap5 компоненты

#### Карточка
```html
<div class="card h-100">
  <img class="card-img-top" src="...">
  <div class="card-body">
    <h5 class="card-title">Заголовок</h5>
    <p>Описание</p>
  </div>
</div>
```

#### Badge (значок)
```html
<span class="badge bg-primary">Тип элемента</span>
<span class="badge bg-secondary">Метка</span>
```

#### Кнопка
```html
<a class="btn btn-primary">Ссылка-кнопка</a>
<button class="btn btn-danger">Кнопка действия</button>
```

#### Alert (уведомление)
```html
<div class="alert alert-info">Информация</div>
<div class="alert alert-warning">Предупреждение</div>
<div class="alert alert-danger">Ошибка</div>
```

---

## Макет и Сетка

### Контейнер
```html
<div class="container">               <!-- max-width: 1200px -->
  <div class="container-fluid">       <!-- width: 100% -->
```

### Сетка (Grid)
```html
<div class="row">
  <div class="col-md-4">33%</div>      <!-- Medium screens -->
  <div class="col-md-4">33%</div>
  <div class="col-md-4">33%</div>
</div>

<div class="row">
  <div class="col-md-7">70%</div>      <!-- Форма админки -->
  <div class="col-md-5">30%</div>      <!-- Preview админки -->
</div>
```

### Отступы
```html
<div class="mb-4">              <!-- margin-bottom -->
<div class="mt-3">              <!-- margin-top -->
<div class="px-5">              <!-- padding horizontal -->
<div class="py-5">              <!-- padding vertical -->
```

### Flexbox
```html
<div class="d-flex justify-content-between align-items-center">
  <h1>Заголовок</h1>
  <a class="btn">Кнопка</a>
</div>

<div class="d-flex gap-2">      <!--间距между элементами -->
  <button>Кнопка 1</button>
  <button>Кнопка 2</button>
</div>
```

---

## Сценарии использования

### 1. Добавление нового элемента

**Процесс:**
1. Админ нажимает "+ Добавить элемент"
2. GET `/admin/{section}/create` → показывает форму
3. Админ заполняет поля, видит preview справа
4. Нажимает "Создать"
5. POST `/admin/{section}/create` → backend создаёт элемент
6. Редирект на `/admin/{section}` → видит новый элемент

**Примечание:** Preview обновляется в реал-тайме через JavaScript

---

### 2. Редактирование элемента

**Процесс:**
1. Админ нажимает "Редактировать" на карточке
2. GET `/admin/{section}/{id}/edit` → показывает форму с текущими данными
3. Админ изменяет данные
4. Нажимает "Сохранить"
5. POST `/admin/{section}/{id}/edit` → backend обновляет
6. Редирект на `/admin/{section}` → видит изменённый элемент

---

### 3. Удаление элемента

**Процесс:**
1. Админ нажимает "Удалить"
2. POST `/admin/{section}/{id}/delete` → backend удаляет
3. Автоматический редирект на `/admin/{section}`

---

### 4. Просмотр главной страницы

**Процесс:**
1. GET `/` → backend получает контент
2. Jinja2 рендерит шаблон с данными
3. Браузер отображает готовую страницу
4. CSS стили применяются автоматически

---

## Инструкции по разработке

### Добавление нового раздела

1. **Добавить в `admin_config.py`:**
```python
ADMIN_CONFIG = {
    "new_section": {
        "fields": ["heading", "text", "image"],
        "types": ["card", "text"],
        "preview": "card"
    }
}
```

2. **Добавить в главный шаблон (`index.html`):**
```html
<section id="new_section">
  <div class="container">
    {% for item in data.new_section %}
      <!-- Рендер элемента -->
    {% endfor %}
  </div>
</section>
```

3. **Добавить ссылку в навигацию:**
```html
<a href="#new_section">Новая секция</a>
```

---

### Кастомизация стилей

**Главная страница:**
Добавить/изменить стили в `static/css/styleHome.css`

**Админка:**
Добавить/изменить стили в `static/css/styleForm.css`

**Использовать Bootstrap классы:**
```html
<div class="text-center mb-4 py-5">
  <h2 class="display-4 fw-bold">Заголовок</h2>
</div>
```

---

### Добавление нового поля в форму

1. **Добавить в конфиг раздела:**
```python
"fields": ["heading", "text", "my_new_field"]
```

2. **Показать в форме (`admin/form.html`):**
```html
{% if "my_new_field" in fields %}
  <div class="mb-3">
    <label>Мое новое поле</label>
    <input type="text" name="my_new_field" 
           oninput="updatePreview()">
  </div>
{% endif %}
```

3. **Показать в предпросмотре (если нужно):**
```html
{% if preview == "card" %}
  <p id="preview-my-field">{{ element.my_new_field }}</p>
{% endif %}
```

---

## Брауэры и совместимость

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

**CSS:** Bootstrap 5 (поддерживает все современные браузеры)

**JavaScript:** Vanilla JS (ES6) — без зависимостей

---

## Производительность

### Оптимизация главной страницы

- **Статика монтируется на `/static`** — кэшируется браузером
- **CSS встроен в дерево** — одна загрузка
- **JavaScript минимален** — только для админки
- **Изображения закодированы в base64** — не требуют доп. запросов

### Время загрузки

- Главная: ~500ms (зависит от БД)
- Админка: ~300ms
- Форма: ~200ms

---

## Возможные улучшения

- [ ] Добавить фильтр поиска элементов в админке
- [ ] Кэширование изображений на диск вместо base64
- [ ] Drag-and-drop для изменения позиций
- [ ] Rich-text editor для текстовых полей
- [ ] Предпросмотр на мобильных экранах
- [ ] Экспорт/импорт контента

---

## Контрольный список для вёрстки

Перед запуском проверить:
- ✅ Все шаблоны синтаксически верны (Jinja2)
- ✅ CSS стили применяются корректно
- ✅ JavaScript функции работают без ошибок
- ✅ Форма передаёт данные на backend
- ✅ Статика монтируется на `/static`
- ✅ Адаптивность на мобильных
- ✅ Предпросмотр обновляется в реал-тайме
- ✅ Редиректы работают корректно
