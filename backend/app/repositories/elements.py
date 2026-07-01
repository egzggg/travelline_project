from sqlalchemy import text
from backend.app.database import engine


def get_elements_by_section(section_name: str):
    """Получить все элементы раздела"""
    with engine.connect() as connection:
        return connection.execute(
            text("""
                SELECT
                    e.element_id,
                    et.name AS type,
                    e.position,
                    e.heading,
                    e.subtitle,
                    e.text,
                    e.label,
                    e.image,
                    e.link
                FROM elements e
                JOIN element_types et ON e.type_id = et.type_id
                JOIN sections s ON e.section_id = s.section_id
                WHERE s.name = :section_name
                ORDER BY e.position
            """),
            {"section_name": section_name}
        ).fetchall()


def get_element_by_id(element_id: int, section_name: str):
    """Получить элемент по ID"""
    with engine.connect() as connection:
        return connection.execute(
            text("""
                SELECT
                    e.element_id,
                    e.position,
                    e.heading,
                    e.subtitle,
                    e.text,
                    e.label,
                    e.image,
                    e.link,
                    et.name AS type
                FROM elements e
                JOIN element_types et ON e.type_id = et.type_id
                JOIN sections s ON e.section_id = s.section_id
                WHERE e.element_id = :id AND s.name = :section
            """),
            {"id": element_id, "section": section_name}
        ).first()


def get_max_position_in_section(section_name: str):
    """Получить максимальную позицию элементов в разделе"""
    with engine.connect() as connection:
        return connection.execute(
            text("""
                SELECT COALESCE(MAX(e.position), 0)
                FROM elements e
                JOIN sections s ON e.section_id = s.section_id
                WHERE s.name = :section
            """),
            {"section": section_name}
        ).scalar()


def get_content_by_sections():
    """Получить все данные для главной страницы"""
    data = {}
    with engine.connect() as connection:
        sections = connection.execute(
            text("""
                SELECT section_id, name
                FROM sections
                ORDER BY section_id
            """)
        ).fetchall()

        for section in sections:
            elements = connection.execute(
                text("""
                    SELECT
                        e.element_id,
                        e.position,
                        e.heading,
                        e.subtitle,
                        e.text,
                        e.label,
                        e.image,
                        e.link,
                        et.name AS type
                    FROM elements e
                    JOIN element_types et ON e.type_id = et.type_id
                    WHERE e.section_id = :section_id
                    ORDER BY e.position
                """),
                {"section_id": section.section_id}
            ).fetchall()

            data[section.name] = [
                {
                    "id": elem.element_id,
                    "position": elem.position,
                    "heading": elem.heading,
                    "subtitle": elem.subtitle,
                    "text": elem.text,
                    "label": elem.label,
                    "image": elem.image,
                    "link": elem.link,
                    "type": elem.type,
                }
                for elem in elements
            ]

    return data


def get_section_id_by_name(section_name: str, connection):
    """Получить ID секции"""
    row = connection.execute(
        text("SELECT section_id FROM sections WHERE name = :name"),
        {"name": section_name}
    ).first()
    return row.section_id if row else None


def get_element_type_id(element_type: str, connection):
    """Получить ID типа элемента"""
    row = connection.execute(
        text("SELECT type_id FROM element_types WHERE name = :name"),
        {"name": element_type}
    ).first()
    return row.type_id if row else None


def count_elements_by_type_in_section(section_name: str, element_type: str, connection, exclude_id: int | None = None):
    """Посчитать количество элементов данного типа в разделе (опционально исключая конкретный элемент)."""
    query = """
        SELECT COUNT(*)
        FROM elements e
        JOIN element_types et ON e.type_id = et.type_id
        JOIN sections s ON e.section_id = s.section_id
        WHERE s.name = :section_name AND et.name = :element_type
    """
    params = {"section_name": section_name, "element_type": element_type}
    if exclude_id is not None:
        query += " AND e.element_id != :exclude_id"
        params["exclude_id"] = exclude_id

    return connection.execute(text(query), params).scalar()


def shift_positions_up(section_id: int, position: int, connection):
    """Сдвинуть позиции элементов вверх"""
    connection.execute(
        text("""
            UPDATE elements
            SET position = position + 1
            WHERE section_id = :section_id AND position >= :position
        """),
        {"section_id": section_id, "position": position}
    )


def shift_positions_down(section_id: int, position: int, connection):
    """Сдвинуть позиции элементов вниз"""
    connection.execute(
        text("""
            UPDATE elements
            SET position = position - 1
            WHERE section_id = :section_id AND position > :position
        """),
        {"section_id": section_id, "position": position}
    )


def create_element(section_id: int, type_id: int, position: int, 
                   heading, subtitle, text_value, label, image, link, connection):
    """Создать новый элемент"""
    connection.execute(
        text("""
            INSERT INTO elements
            (section_id, type_id, position, heading, subtitle, text, label, image, link)
            VALUES (:section_id, :type_id, :position, :heading, :subtitle, :text, :label, :image, :link)
        """),
        {
            "section_id": section_id,
            "type_id": type_id,
            "position": position,
            "heading": heading,
            "subtitle": subtitle,
            "text": text_value,
            "label": label,
            "image": image,
            "link": link
        }
    )


def delete_element(element_id: int, connection):
    """Удалить элемент"""
    connection.execute(
        text("DELETE FROM elements WHERE element_id = :id"),
        {"id": element_id}
    )


def update_element(element_id: int, type_id: int, position: int,
                   heading, subtitle, text_value, label, image, link, connection):
    """Обновить элемент"""
    connection.execute(
        text("""
            UPDATE elements
            SET type_id=:type_id, position=:position, heading=:heading,
                subtitle=:subtitle, text=:text, label=:label,
                image=:image, link=:link
            WHERE element_id=:id
        """),
        {
            "type_id": type_id,
            "position": position,
            "heading": heading,
            "subtitle": subtitle,
            "text": text_value,
            "label": label,
            "image": image,
            "link": link,
            "id": element_id
        }
    )


def get_element_at_position(section_id: int, position: int, element_id: int, connection):
    """Получить элемент на определённой позиции"""
    row = connection.execute(
        text("""
            SELECT element_id FROM elements
            WHERE section_id = :section_id AND position = :position AND element_id != :id
        """),
        {"section_id": section_id, "position": position, "id": element_id}
    ).first()
    return row.element_id if row else None


def get_old_element_data(element_id: int, connection):
    """Получить старые данные элемента"""
    return connection.execute(
        text("""
            SELECT position, heading, subtitle, text, label, image, link
            FROM elements
            WHERE element_id = :id
        """),
        {"id": element_id}
    ).first()
