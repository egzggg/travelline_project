from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import text

from backend.app.database import engine


app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent.parent.parent


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