from sqlalchemy import text

from backend.app.database import engine


def upgrade():

    with engine.begin() as connection:

        # -----------------------------
        # Таблица секций
        # -----------------------------

        connection.execute(text("""
        CREATE TABLE IF NOT EXISTS sections
        (
            section_id SERIAL PRIMARY KEY,

            name VARCHAR(100)
            NOT NULL
            UNIQUE
        );
        """))


        # -----------------------------
        # Типы элементов
        # -----------------------------

        connection.execute(text("""
        CREATE TABLE IF NOT EXISTS element_types
        (
            type_id SERIAL PRIMARY KEY,

            name VARCHAR(50)
            NOT NULL
            UNIQUE
        );
        """))


        # -----------------------------
        # Элементы секций
        # -----------------------------

        connection.execute(text("""
        CREATE TABLE IF NOT EXISTS elements
        (
            element_id SERIAL PRIMARY KEY,


            section_id INTEGER
            NOT NULL,


            type_id INTEGER
            NOT NULL,


            position INTEGER
            NOT NULL,


            heading TEXT,

            text TEXT,

            image TEXT,

            link TEXT,


            CONSTRAINT fk_element_section
            FOREIGN KEY(section_id)
            REFERENCES sections(section_id)
            ON DELETE CASCADE,


            CONSTRAINT fk_element_type
            FOREIGN KEY(type_id)
            REFERENCES element_types(type_id)
        );
        """))


        # -----------------------------
        # Начальные типы элементов
        # -----------------------------

        connection.execute(text("""
        INSERT INTO element_types(name)
        VALUES
            ('text'),
            ('button'),
            ('image'),
            ('link')
        ON CONFLICT (name) DO NOTHING;
        """))



def downgrade():

    with engine.begin() as connection:

        connection.execute(text("""
        DROP TABLE IF EXISTS elements CASCADE;
        """))


        connection.execute(text("""
        DROP TABLE IF EXISTS element_types CASCADE;
        """))


        connection.execute(text("""
        DROP TABLE IF EXISTS sections CASCADE;
        """))



if __name__ == "__main__":
    upgrade()