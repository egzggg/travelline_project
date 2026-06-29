| Раздел                       | Элементы                                                                                |
| ---------------------------- | --------------------------------------------------------------------------------------- |
| **Hero**                     | Заголовок, подзаголовок, статистика (каждая цифра отдельным элементом)                  |
| **Team**                     | Имя, должность, фото, ссылка на соцсеть                                                 |
| **Timeline**                 | Год, название продукта, описание, тип метки                                             |
| **Clients** *(новый раздел)* | Название клиента, логотип                                                               |
| **Directions**               | Название направления, описание, технологии (можно одной строкой или отдельной таблицей) |
| **Vacancies**                | Название вакансии, формат работы, ссылка                                                |
| **Gallery** *(новый раздел)* | Подпись, изображение (или видео)                                                        |
| **Offices**                  | Город, описание, фото                                                                   |
| **Benefits**                 | Заголовок, описание                                                                     |
| **Contact**                  | Заголовок, подзаголовок, текст кнопки                                                   |

```sql
-- ===========================================
-- Roles
-- ===========================================

CREATE TABLE roles
(
    role_id SERIAL PRIMARY KEY,

    name VARCHAR(50)
    NOT NULL
    UNIQUE
);


-- ===========================================
-- Users
-- ===========================================

CREATE TABLE users
(
    user_id SERIAL PRIMARY KEY,

    role_id INTEGER
    NOT NULL,

    name VARCHAR(255)
    NOT NULL,

    login VARCHAR(255)
    NOT NULL
    UNIQUE,

    password VARCHAR(255)
    NOT NULL,

    CONSTRAINT fk_users_role
        FOREIGN KEY (role_id)
        REFERENCES roles(role_id)
        ON DELETE RESTRICT
);


-- ===========================================
-- Sections
-- ===========================================

CREATE TABLE sections
(
    section_id SERIAL PRIMARY KEY,

    name VARCHAR(100)
    NOT NULL
    UNIQUE
);


-- ===========================================
-- Element types
-- ===========================================

CREATE TABLE element_types
(
    type_id SERIAL PRIMARY KEY,

    name VARCHAR(50)
    NOT NULL
    UNIQUE
);


-- ===========================================
-- Elements
-- ===========================================

CREATE TABLE elements
(
    element_id SERIAL PRIMARY KEY,

    section_id INTEGER
    NOT NULL,

    type_id INTEGER
    NOT NULL,

    position INTEGER
    NOT NULL,

    heading TEXT,

    subtitle TEXT,

    text TEXT,

    label TEXT,

    image TEXT,

    link TEXT,

    CONSTRAINT fk_elements_section
        FOREIGN KEY (section_id)
        REFERENCES sections(section_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_elements_type
        FOREIGN KEY (type_id)
        REFERENCES element_types(type_id)
);


-- ===========================================
-- Default element types
-- ===========================================

INSERT INTO element_types(name)
VALUES
    ('text'),
    ('button'),
    ('card'),
    ('image'),
    ('link')
ON CONFLICT (name) DO NOTHING;


-- ===========================================
-- Default sections
-- ===========================================

INSERT INTO sections(name)
VALUES
    ('hero'),
    ('statistics'),
    ('team'),
    ('timeline'),
    ('clients'),
    ('directions'),
    ('vacancies'),
    ('gallery'),
    ('offices'),
    ('benefits'),
    ('contact')
ON CONFLICT (name) DO NOTHING;
```
