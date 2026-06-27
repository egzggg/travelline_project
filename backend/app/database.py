import os

from sqlalchemy import create_engine


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://travelline_user:travelline_pass@localhost:5435/travelline"
)


engine = create_engine(
    DATABASE_URL
)