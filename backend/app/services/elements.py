from sqlalchemy import text
from backend.app.database import engine
from backend.app.repositories import elements as repo
from backend.app.utils.files import encode_image_to_base64


async def create_element_service(
    section_name: str,
    element_type: str,
    position: int,
    heading,
    subtitle,
    text_value,
    label,
    link,
    image,
    config
):
    """Создать новый элемент"""
    image_base64 = await encode_image_to_base64(image) if image else None

    # Фильтрация полей через ADMIN_CONFIG
    if "heading" not in config["fields"]:
        heading = None
    if "subtitle" not in config["fields"]:
        subtitle = None
    if "text" not in config["fields"]:
        text_value = None
    if "label" not in config["fields"]:
        label = None
    if "link" not in config["fields"]:
        link = None
    if "image" not in config["fields"]:
        image_base64 = None

    with engine.begin() as connection:
        section_row = connection.execute(
            text("SELECT section_id FROM sections WHERE name = :name"),
            {"name": section_name}
        ).first()
        
        if not section_row:
            return None, "Section not found"
        
        section_id = section_row.section_id

        type_row = connection.execute(
            text("SELECT type_id FROM element_types WHERE name = :name"),
            {"name": element_type}
        ).first()
        
        if not type_row:
            return None, "Element type not found"

        if position < 1:
            return None, "Invalid position"

        max_position = repo.get_max_position_in_section(section_name)
        if position > max_position + 1:
            return None, "Invalid position"

        # Валидация для раздела contact: максимум по одному элементу типов title и button
        if section_name == "contact":
            if element_type in ("title", "button"):
                existing = repo.count_elements_by_type_in_section(section_name, element_type, connection)
                if existing >= 1:
                    return None, f"Only one element of type '{element_type}' is allowed in contact"

        # Если создаётся button — игнорируем heading
        if element_type == "button":
            heading = None

        # Сдвигаем позиции
        repo.shift_positions_up(section_id, position, connection)

        # Создаём элемент
        repo.create_element(
            section_id, type_row.type_id, position,
            heading, subtitle, text_value, label, image_base64, link,
            connection
        )

    return True, "Element created successfully"


async def update_element_service(
    section_name: str,
    element_id: int,
    element_type: str,
    position: int,
    heading,
    subtitle,
    text_value,
    label,
    link,
    image,
    config
):
    """Обновить элемент"""
    image_base64 = await encode_image_to_base64(image) if image and image.filename else None

    with engine.begin() as connection:
        old_element = repo.get_old_element_data(element_id, connection)
        if not old_element:
            return None, "Element not found"

        # Заполняем пустые значения старыми
        if not heading:
            heading = old_element.heading
        if not subtitle:
            subtitle = old_element.subtitle
        if not text_value:
            text_value = old_element.text
        if not label:
            label = old_element.label
        if not link:
            link = old_element.link
        if not image_base64:
            image_base64 = old_element.image

        old_position = old_element.position

        # Если позиция изменилась
        if old_position != position:
            section_row = connection.execute(
                text("SELECT section_id FROM elements WHERE element_id = :id"),
                {"id": element_id}
            ).first()
            
            another_row = connection.execute(
                text("""
                    SELECT element_id FROM elements
                    WHERE section_id = :section_id AND position = :position AND element_id != :id
                """),
                {"section_id": section_row.section_id, "position": position, "id": element_id}
            ).first()

            if another_row:
                connection.execute(
                    text("UPDATE elements SET position = :old_position WHERE element_id = :id"),
                    {"old_position": old_position, "id": another_row.element_id}
                )

        type_row = connection.execute(
            text("SELECT type_id FROM element_types WHERE name = :name"),
            {"name": element_type}
        ).first()
        # Валидация для раздела contact при обновлении: максимум по одному title/button
        if section_name == "contact":
            if element_type == "button":
                heading = None

            existing = repo.count_elements_by_type_in_section(section_name, element_type, connection, exclude_id=element_id)
            if existing >= 1:
                return None, f"Only one element of type '{element_type}' is allowed in contact"

        repo.update_element(
            element_id, type_row.type_id, position,
            heading, subtitle, text_value, label, image_base64, link,
            connection
        )

    return True, "Element updated successfully"


async def delete_element_service(
    section_name: str,
    element_id: int
):
    """Удалить элемент"""
    with engine.begin() as connection:
        element = connection.execute(
            text("""
                SELECT element_id, section_id, position
                FROM elements
                WHERE element_id = :id
            """),
            {"id": element_id}
        ).first()

        if not element:
            return None, "Element not found"

        repo.delete_element(element_id, connection)
        repo.shift_positions_down(element.section_id, element.position, connection)

    return True, "Element deleted successfully"
