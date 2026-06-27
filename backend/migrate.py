import importlib


MIGRATIONS = [
    "backend.migrations.001_create_users_roles",
    "backend.migrations.002_create_sections_elements",
    "backend.migrations.003_seed_users_roles",
    "backend.migrations.004_seed_site_content",
]


def run_migrations():

    print("Starting migrations...")


    for migration_name in MIGRATIONS:

        print(f"\nRunning {migration_name}")

        migration = importlib.import_module(migration_name)

        migration.upgrade()

        print("OK")

    print("\nAll migrations completed successfully.")



if __name__ == "__main__":
    run_migrations()