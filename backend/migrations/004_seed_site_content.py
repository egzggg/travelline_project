from pathlib import Path
import json

from sqlalchemy import text

from backend.app.database import engine


BASE_DIR = Path(__file__).resolve().parent.parent.parent

JSON_PATH = BASE_DIR / "json" / "struct_json.json"


def upgrade():

    with open(JSON_PATH, encoding="utf-8") as file:
        data = json.load(file)


    with engine.begin() as connection:

        section_ids = {}


        # -----------------------------
        # Создаем секции
        # -----------------------------

        for section_name in data.keys():

            result = connection.execute(
                text("""
                    INSERT INTO sections(name)
                    VALUES (:name)
                    RETURNING section_id;
                """),
                {
                    "name": section_name
                }
            )

            section_ids[section_name] = result.scalar()



        # -----------------------------
        # Получаем типы элементов
        # -----------------------------

        types = {}

        result = connection.execute(
            text("""
                SELECT type_id, name
                FROM element_types;
            """)
        )


        for row in result:
            types[row.name] = row.type_id



        # -----------------------------
        # Создаем элементы
        # -----------------------------

        for section_name, content in data.items():

            section_id = section_ids[section_name]


            for element in content:


                element_type = element.get("type")


                type_id = types.get(element_type)


                connection.execute(
                    text("""
                        INSERT INTO elements
                        (
                            section_id,
                            type_id,
                            position,
                            heading,
                            text,
                            image,
                            link
                        )
                        VALUES
                        (
                            :section_id,
                            :type_id,
                            :position,
                            :heading,
                            :text,
                            :image,
                            :link
                        );
                    """),
                    {
                        "section_id": section_id,
                        "type_id": type_id,
                        "position": element.get("position"),
                        "heading": element.get("heading"),
                        "text": element.get("text"),
                        "image": element.get("image"),
                        "link": element.get("link")
                    }
                )



def downgrade():

    with engine.begin() as connection:

        connection.execute(
            text("""
                DELETE FROM elements;
            """)
        )


        connection.execute(
            text("""
                DELETE FROM sections;
            """)
        )


if __name__ == "__main__":
    upgrade()