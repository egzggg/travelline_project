# Ошибка: TypeError: unhashable type: 'dict'## СимптомFastAPI запускался нормально, JSON успешно загружался, но при открытии `/` получался:
Internal Server Error
TypeError: unhashable type: 'dict'
## ПричинаНеверный вызов `TemplateResponse`.Использовался старый формат:```pythontemplates.TemplateResponse(    "index.html",    {        "request": request,        "data": data    })
В новых версиях FastAPI/Starlette аргументы изменились, из-за чего Jinja2 получал словарь вместо имени шаблона.
Исправление
Использовать явные параметры:
templates.TemplateResponse(    request=request,    name="index.html",    context={        "data": data    })
Как избежать


Проверять изменения API после обновления библиотек.


Использовать именованные аргументы вместо позиционных.


При ошибках Jinja2 сначала проверять:


путь к шаблонам;


имя HTML файла;


передачу context в TemplateResponse.




Вывод
Проблема была не в JSON и не в структуре проекта.
Ошибка возникла из-за несовместимого синтаксиса TemplateResponse в новой версии Starlette.


# PostgreSQL 18 Docker volume error

## Ошибка

После смены образа PostgreSQL на 18 контейнер уходит в Restarting.

Ошибка:

"there appears to be PostgreSQL data in /var/lib/postgresql/data"

## Причина

PostgreSQL 18 изменил структуру хранения данных.
Старые volumes от PostgreSQL 16/17 несовместимы с новым образом.

## Решение

Для новой базы удалить старый volume:

docker compose down -v

Для PostgreSQL 18 использовать:

/var/lib/postgresql

вместо:

/var/lib/postgresql/data

## Как избежать

При смене major-версии PostgreSQL:
- не использовать старый volume напрямую
- выполнять pg_upgrade
- либо создавать новый volume