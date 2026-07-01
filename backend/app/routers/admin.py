from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from backend.app.admin_config import ADMIN_CONFIG
from backend.app.repositories import elements as repo
from backend.app.services import elements as elem_service

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

templates = Jinja2Templates(directory=str(BASE_DIR / "frontend/templates"))

router = APIRouter()


@router.get("/admin", response_class=HTMLResponse)
async def admin_list(request: Request):
    """Список разделов админки"""
    sections = [
        {"name": name.capitalize(), "slug": name}
        for name in ADMIN_CONFIG.keys()
    ]

    return templates.TemplateResponse(
        request=request,
        name="admin/index.html",
        context={"sections": sections}
    )


@router.get("/admin/{section_name}", response_class=HTMLResponse)
async def admin_section(request: Request, section_name: str):
    """Список элементов в разделе"""
    config = ADMIN_CONFIG.get(section_name)

    if not config:
        return HTMLResponse("Section configuration not found", status_code=404)

    elements = repo.get_elements_by_section(section_name)
    elements_list = [
        {
            "id": elem.element_id,
            "type": elem.type,
            "position": elem.position,
            "heading": elem.heading,
            "subtitle": elem.subtitle,
            "text": elem.text,
            "label": elem.label,
            "image": elem.image,
            "link": elem.link,
        }
        for elem in elements
    ]

    return templates.TemplateResponse(
        request=request,
        name="admin/section.html",
        context={"section_name": section_name, "elements": elements_list}
    )


@router.get("/admin/{section_name}/create", response_class=HTMLResponse)
async def admin_create_form(request: Request, section_name: str):
    """Форма создания элемента"""
    config = ADMIN_CONFIG.get(section_name)

    if not config:
        return HTMLResponse("Section configuration not found", status_code=404)

    max_position = repo.get_max_position_in_section(section_name)

    return templates.TemplateResponse(
        request=request,
        name="admin/form.html",
        context={
            "mode": "create",
            "title": "Создание элемента",
            "button": "Создать",
            "section_name": section_name,
            "element": None,
            "fields": config["fields"],
            "types": config["types"],
            "preview": config["preview"],
            "positions": list(range(1, max_position + 2)),
            "default_position": max_position + 1,
        }
    )


@router.post("/admin/{section_name}/create")
async def admin_create_post(
    section_name: str,
    element_type: str = Form(...),
    position: int = Form(...),
    heading: str | None = Form(None),
    subtitle: str | None = Form(None),
    text_value: str | None = Form(None, alias="text"),
    label: str | None = Form(None),
    link: str | None = Form(None),
    image: UploadFile | None = File(None),
):
    """Сохранить новый элемент"""
    config = ADMIN_CONFIG.get(section_name)

    if not config:
        return HTMLResponse("Section configuration not found", status_code=404)

    if element_type not in config["types"]:
        return HTMLResponse("This element type is not allowed for this section", status_code=400)

    success, message = await elem_service.create_element_service(
        section_name, element_type, position,
        heading, subtitle, text_value, label, link, image, config
    )

    if not success:
        return HTMLResponse(message, status_code=400)

    return RedirectResponse(url=f"/admin/{section_name}", status_code=303)


@router.get("/admin/{section_name}/{element_id}/edit", response_class=HTMLResponse)
async def admin_edit_form(request: Request, section_name: str, element_id: int):
    """Форма редактирования элемента"""
    config = ADMIN_CONFIG.get(section_name)

    if not config:
        return HTMLResponse("Section configuration not found", status_code=404)

    element = repo.get_element_by_id(element_id, section_name)

    if not element:
        return HTMLResponse("Element not found", status_code=404)

    max_position = repo.get_max_position_in_section(section_name)

    return templates.TemplateResponse(
        request=request,
        name="admin/form.html",
        context={
            "mode": "edit",
            "title": "Редактирование элемента",
            "button": "Сохранить",
            "section_name": section_name,
            "element": element,
            "fields": config["fields"],
            "types": config["types"],
            "preview": config["preview"],
            "positions": list(range(1, max_position + 1)),
            "default_position": element.position,
        }
    )


@router.post("/admin/{section_name}/{element_id}/edit")
async def admin_edit_post(
    section_name: str,
    element_id: int,
    element_type: str = Form(...),
    position: int = Form(...),
    heading: str | None = Form(None),
    subtitle: str | None = Form(None),
    text_value: str | None = Form(None, alias="text"),
    label: str | None = Form(None),
    link: str | None = Form(None),
    image: UploadFile | None = File(None),
):
    """Сохранить изменения элемента"""
    config = ADMIN_CONFIG.get(section_name)

    if not config:
        return HTMLResponse("Section configuration not found", status_code=404)

    if element_type not in config["types"]:
        return HTMLResponse("Invalid type", status_code=400)

    success, message = await elem_service.update_element_service(
        section_name, element_id, element_type, position,
        heading, subtitle, text_value, label, link, image, config
    )

    if not success:
        return HTMLResponse(message, status_code=400)

    return RedirectResponse(url=f"/admin/{section_name}", status_code=303)


@router.post("/admin/{section_name}/{element_id}/delete")
async def admin_delete(section_name: str, element_id: int):
    """Удалить элемент"""
    config = ADMIN_CONFIG.get(section_name)

    if not config:
        return HTMLResponse("Section configuration not found", status_code=404)

    success, message = await elem_service.delete_element_service(section_name, element_id)

    if not success:
        return HTMLResponse(message, status_code=400)

    return RedirectResponse(url=f"/admin/{section_name}", status_code=303)
