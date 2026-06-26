from sqlalchemy import text

from backend.app.database import engine


def upgrade():

    with engine.begin() as connection:


        connection.execute(text("""
        CREATE TABLE sections
        (
            section_id SERIAL PRIMARY KEY,

            name VARCHAR(100)
            NOT NULL
            UNIQUE
        );
        """))



        connection.execute(text("""
        CREATE TABLE element_types
        (
            type_id SERIAL PRIMARY KEY,

            name VARCHAR(50)
            NOT NULL
            UNIQUE
        );
        """))



        connection.execute(text("""
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



        connection.execute(text("""
        INSERT INTO element_types(name)
        VALUES
        ('text'),
        ('button'),
        ('image'),
        ('link');
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