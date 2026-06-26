from sqlalchemy import text

from backend.app.database import engine


def upgrade():

    with engine.begin() as connection:

        connection.execute(text("""
        CREATE TABLE roles
        (
            role_id SERIAL PRIMARY KEY,

            name VARCHAR(50)
            NOT NULL
            UNIQUE
        );
        """))


        connection.execute(text("""
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
            FOREIGN KEY(role_id)
            REFERENCES roles(role_id)
        );
        """))


def downgrade():

    with engine.begin() as connection:
        connection.execute(text("""
        DROP TABLE IF EXISTS users CASCADE;
        """))

        connection.execute(text("""
        DROP TABLE IF EXISTS roles CASCADE;
        """))


if __name__ == "__main__":
    upgrade()