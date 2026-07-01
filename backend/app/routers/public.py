from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from backend.app.repositories.elements import get_content_by_sections

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

templates = Jinja2Templates(directory=str(BASE_DIR / "frontend/templates"))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Главная страница"""
    data = get_content_by_sections()
    
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"data": data}
    )


@router.get("/api/content")
async def get_content():
    """API для получения контента"""
    return get_content_by_sections()
