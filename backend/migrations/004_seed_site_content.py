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


        # -----------------------------
        # Получаем типы элементов
        # -----------------------------

        types = {}


        result = connection.execute(
            text(
                """
                SELECT
                    type_id,
                    name
                FROM element_types;
                """
            )
        )


        for row in result:

            types[row.name] = row.type_id




        # -----------------------------
        # Получаем секции
        # -----------------------------

        sections = {}


        result = connection.execute(
            text(
                """
                SELECT
                    section_id,
                    name
                FROM sections;
                """
            )
        )


        for row in result:

            sections[row.name] = row.section_id





        # -----------------------------
        # Заполняем контент
        # -----------------------------

        for section_name, elements in data.items():


            section_id = sections.get(section_name)



            if section_id is None:

                raise Exception(
                    f"Unknown section: {section_name}"
                )



            for element in elements:


                element_type = element.get("type")



                type_id = types.get(element_type)



                if type_id is None:

                    raise Exception(
                        f"Unknown element type: {element_type}"
                    )




                connection.execute(
                    text(
                        """
                        INSERT INTO elements
                        (
                            section_id,

                            type_id,

                            position,

                            heading,
                            subtitle,
                            text,
                            label,
                            image,
                            link
                        )


                        VALUES
                        (
                            :section_id,

                            :type_id,

                            :position,

                            :heading,

                            :subtitle,

                            :text,

                            :label,

                            :image,

                            :link
                        );
                        """
                    ),
                    {

                        "section_id": section_id,

                        "type_id": type_id,

                        "position": element.get(
                            "position",
                            1
                        ),

                        "heading": element.get(
                            "heading"
                        ),

                        "subtitle": element.get(
                            "subtitle"
                        ),

                        "text": element.get(
                            "text"
                        ),

                        "label": element.get(
                            "label"
                        ),

                        "image": element.get(
                            "image"
                        ),

                        "link": element.get(
                            "link"
                        )

                    }
                )





def downgrade():

    with engine.begin() as connection:


        connection.execute(
            text(
                """
                DELETE FROM elements;
                """
            )
        )



if __name__ == "__main__":

    upgrade()