from sqlalchemy import text

from backend.app.database import engine


def upgrade():

    with engine.begin() as connection:

        # -----------------------------
        # Roles
        # -----------------------------

        connection.execute(
            text(
                """
                INSERT INTO roles (name)
                VALUES
                    ('admin'),
                    ('user');
                """
            )
        )

        # -----------------------------
        # Users
        # -----------------------------

        admin_role = connection.execute(
            text(
                """
                SELECT role_id
                FROM roles
                WHERE name = 'admin';
                """
            )
        ).scalar()

        user_role = connection.execute(
            text(
                """
                SELECT role_id
                FROM roles
                WHERE name = 'user';
                """
            )
        ).scalar()

        connection.execute(
            text(
                """
                INSERT INTO users
                (
                    role_id,
                    name,
                    login,
                    password
                )
                VALUES
                (
                    :role_id,
                    :name,
                    :login,
                    :password
                )
                """
            ),
            {
                "role_id": admin_role,
                "name": "Administrator",
                "login": "admin",
                "password": "admin"
            }
        )

        connection.execute(
            text(
                """
                INSERT INTO users
                (
                    role_id,
                    name,
                    login,
                    password
                )
                VALUES
                (
                    :role_id,
                    :name,
                    :login,
                    :password
                )
                """
            ),
            {
                "role_id": user_role,
                "name": "Default User",
                "login": "user",
                "password": "user"
            }
        )


def downgrade():

    with engine.begin() as connection:

        connection.execute(text("DELETE FROM users;"))
        connection.execute(text("DELETE FROM roles;"))
if __name__ == "__main__":
    upgrade()