from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import text

from backend.app.database import engine


app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent.parent.parent

ADMIN_SECTIONS = [
    ("Header", "header"),
    ("Hero", "hero"),
    ("Statistics", "statistics"),
    ("Team", "team"),
    ("Timeline", "timeline"),
    ("Directions", "directions"),
    ("Vacancies", "vacancies"),
    ("Offices", "offices"),
    ("Benefits", "benefits"),
    ("Contact Form", "contact"),
    ("Footer", "footer")
]


templates = Jinja2Templates(
    directory=str(BASE_DIR / "frontend/templates")
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    data = {}

    with engine.connect() as connection:

        sections = connection.execute(
            text(
                """
                SELECT 
                    section_id,
                    name
                FROM sections
                ORDER BY section_id
                """
            )
        )


        for section in sections:

            elements = connection.execute(
                text(
                    """
                    SELECT
                        e.element_id,
                        e.position,
                        e.heading,
                        e.text,
                        e.image,
                        e.link,
                        et.name AS type
                    FROM elements e
                    JOIN element_types et
                    ON e.type_id = et.type_id
                    WHERE e.section_id = :section_id
                    ORDER BY e.position
                    """
                ),
                {
                    "section_id": section.section_id
                }
            )


            data[section.name] = []


            for element in elements:

                data[section.name].append(
                    {
                        "id_element": element.element_id,
                        "position": element.position,
                        "heading": element.heading,
                        "text": element.text,
                        "image": element.image,
                        "link": element.link,
                        "type": element.type
                    }
                )


    print(data)


    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "data": data
        }
    )

@app.get("/api/content")
async def get_content():

    data = {}

    with engine.connect() as connection:

        sections = connection.execute(
            text("""
                SELECT 
                    section_id,
                    name
                FROM sections
                ORDER BY section_id
            """)
        )


        for section in sections:

            elements = connection.execute(
                text("""
                    SELECT
                        element_id,
                        position,
                        heading,
                        text,
                        image,
                        link,
                        element_types.name AS type
                    FROM elements

                    JOIN element_types
                    ON elements.type_id = element_types.type_id

                    WHERE section_id = :section_id

                    ORDER BY position
                """),
                {
                    "section_id": section.section_id
                }
            )


            data[section.name] = []


            for element in elements:

                data[section.name].append(
                    {
                        "id": element.element_id,
                        "position": element.position,
                        "heading": element.heading,
                        "text": element.text,
                        "image": element.image,
                        "link": element.link,
                        "type": element.type
                    }
                )


    return data

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="admin/index.html",
        context={
            "sections": ADMIN_SECTIONS
        }
    )

@app.get("/admin/{section_name}", response_class=HTMLResponse)
async def admin_section(request: Request, section_name: str):

    with engine.connect() as connection:

        elements = connection.execute(
            text(
                """
                SELECT
                    e.element_id,
                    et.name AS type,
                    e.position,
                    e.heading,
                    e.text,
                    e.image,
                    e.link
                FROM elements e
                JOIN element_types et
                    ON e.type_id = et.type_id
                JOIN sections s
                    ON e.section_id = s.section_id
                WHERE s.name = :section_name
                ORDER BY e.position;
                """
            ),
            {
                "section_name": section_name
            }
        )

        data = []

        for element in elements:

            data.append(
                {
                    "id": element.element_id,
                    "type": element.type,
                    "position": element.position,
                    "heading": element.heading,
                    "text": element.text,
                    "image": element.image,
                    "link": element.link
                }
            )

    return templates.TemplateResponse(
        request=request,
        name="admin/section.html",
        context={
            "section_name": section_name,
            "elements": data
        }
    )