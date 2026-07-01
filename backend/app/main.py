from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.app.routers import public, admin

BASE_DIR = Path(__file__).resolve().parent.parent.parent

app = FastAPI()

# Монтируем статику
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "frontend/static")),
    name="static",
)

# Включаем маршруты
app.include_router(public.router)
app.include_router(admin.router)
