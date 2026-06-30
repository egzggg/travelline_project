from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from sqlalchemy import text

from fastapi import Form, UploadFile, File
from fastapi.responses import RedirectResponse
import base64

from backend.app.database import engine
from backend.app.admin_config import ADMIN_CONFIG

app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent.parent.parent

ADMIN_SECTIONS = [
    (name.capitalize(), name)
    for name in ADMIN_CONFIG.keys()
]


app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "frontend/static")),
    name="static",
)


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
                        e.subtitle,
                        e.text,
                        e.label,

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

                        "id": element.element_id,

                        "position": element.position,

                        "heading": element.heading,

                        "subtitle": element.subtitle,

                        "text": element.text,

                        "label": element.label,

                        "image": element.image,

                        "link": element.link,

                        "type": element.type

                    }
                )



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
                        e.subtitle,
                        e.text,
                        e.label,

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
                        "id": element.element_id,

                        "position": element.position,

                        "heading": element.heading,

                        "subtitle": element.subtitle,

                        "text": element.text,

                        "label": element.label,

                        "image": element.image,

                        "link": element.link,

                        "type": element.type
                    }
                )


    return data



@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    print(ADMIN_CONFIG.keys())


    sections = [
        {
            "name": name.capitalize(),
            "slug": name
        }

        for name in ADMIN_CONFIG.keys()
    ]



    return templates.TemplateResponse(

        request=request,

        name="admin/index.html",

        context={
            "sections": sections
        }

    )






@app.get("/admin/{section_name}", response_class=HTMLResponse)
async def admin_section(
    request: Request,
    section_name: str
):


    config = ADMIN_CONFIG.get(section_name)


    if not config:

        return HTMLResponse(
            "Section configuration not found",
            status_code=404
        )



    with engine.connect() as connection:


        elements = connection.execute(
            text(
                """
                SELECT

                    e.element_id,

                    et.name AS type,

                    e.position,

                    e.heading,
                    e.subtitle,
                    e.text,
                    e.label,

                    e.image,
                    e.link


                FROM elements e


                JOIN element_types et
                ON e.type_id = et.type_id


                JOIN sections s
                ON e.section_id = s.section_id


                WHERE s.name = :section_name


                ORDER BY e.position

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

                    "subtitle": element.subtitle,

                    "text": element.text,

                    "label": element.label,

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








@app.get("/admin/{section_name}/create", response_class=HTMLResponse)
async def admin_create_element(
    request: Request,
    section_name: str
):


    config = ADMIN_CONFIG.get(section_name)



    if not config:

        return HTMLResponse(
            "Section configuration not found",
            status_code=404
        )



    with engine.connect() as connection:


        max_position = connection.execute(
            text(
                """
                SELECT COALESCE(MAX(e.position),0)

                FROM elements e

                JOIN sections s
                ON e.section_id = s.section_id

                WHERE s.name = :section_name

                """
            ),
            {
                "section_name": section_name
            }
        ).scalar()



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


            "positions": list(
                range(
                    1,
                    max_position + 2
                )
            ),


            "default_position": max_position + 1

        }

    )

@app.post("/admin/{section_name}/create")
async def admin_create_element_post(
    request: Request,
    section_name: str,

    element_type: str = Form(...),
    position: int = Form(...),

    heading: str | None = Form(None),
    subtitle: str | None = Form(None),
    text_value: str | None = Form(None, alias="text"),
    label: str | None = Form(None),
    link: str | None = Form(None),

    image: UploadFile | None = File(None)
):
    form = await request.form()
    print(form)


    config = ADMIN_CONFIG.get(section_name)



    if not config:

        return HTMLResponse(
            "Section configuration not found",
            status_code=404
        )





    if element_type not in config["types"]:

        return HTMLResponse(
            "This element type is not allowed for this section",
            status_code=400
        )





    image_base64 = None



    if image:


        content = await image.read()


        image_base64 = (

            "data:"

            + image.content_type

            + ";base64,"

            + base64.b64encode(content).decode()

        )







    # фильтрация полей через ADMIN_CONFIG


    if "heading" not in config["fields"]:

        heading = None



    if "subtitle" not in config["fields"]:

        subtitle = None



    if "text" not in config["fields"]:
        text_value = None



    if "label" not in config["fields"]:

        label = None



    if "link" not in config["fields"]:

        link = None



    if "image" not in config["fields"]:

        image_base64 = None







    with engine.begin() as connection:



        section = connection.execute(

            text(

                """
                SELECT section_id

                FROM sections

                WHERE name = :name
                """

            ),

            {
                "name": section_name
            }

        ).first()





        if not section:


            return HTMLResponse(

                "Section not found",

                status_code=404

            )





        section_id = section.section_id







        max_position = connection.execute(

            text(

                """
                SELECT COALESCE(MAX(position),0)

                FROM elements

                WHERE section_id = :section_id
                """

            ),

            {
                "section_id": section_id
            }

        ).scalar()







        if position < 1 or position > max_position + 1:


            return HTMLResponse(

                "Invalid position",

                status_code=400

            )







        element_type_row = connection.execute(

            text(

                """
                SELECT type_id

                FROM element_types

                WHERE name = :name
                """

            ),

            {
                "name": element_type
            }

        ).first()






        if not element_type_row:


            return HTMLResponse(

                "Element type not found",

                status_code=404

            )





        connection.execute(

            text(

                """
                UPDATE elements

                SET position = position + 1

                WHERE section_id = :section_id

                AND position >= :position
                """

            ),

            {

                "section_id": section_id,

                "position": position

            }

        )







        connection.execute(

            text(

                """
                INSERT INTO elements
                (
                    section_id,

                    type_id,

                    position,

                    heading,

                    subtitle,

                    text,

                    label,

                    image,

                    link
                )

                VALUES
                (
                    :section_id,

                    :type_id,

                    :position,

                    :heading,

                    :subtitle,

                    :text,

                    :label,

                    :image,

                    :link
                )

                """

            ),

            {


                "section_id": section_id,


                "type_id": element_type_row.type_id,


                "position": position,


                "heading": heading,


                "subtitle": subtitle,


                "text": text_value,


                "label": label,


                "image": image_base64,


                "link": link


            }

        )
        result = connection.execute(
            text("""
                SELECT *
                FROM elements
                ORDER BY element_id DESC
                LIMIT 1
            """)
        )

        print(result.first())





    return RedirectResponse(

        url=f"/admin/{section_name}",

        status_code=303

    )

@app.get(
    "/admin/{section_name}/{element_id}/edit",
    response_class=HTMLResponse
)
async def admin_edit_element(
    request: Request,
    section_name: str,
    element_id: int
):

    config = ADMIN_CONFIG.get(section_name)


    if not config:

        return HTMLResponse(
            "Section configuration not found",
            status_code=404
        )



    with engine.connect() as connection:


        element = connection.execute(
            text(
                """
                SELECT

                    e.element_id,

                    e.position,

                    e.heading,

                    e.subtitle,

                    e.text,

                    e.label,

                    e.image,

                    e.link,

                    et.name AS type


                FROM elements e


                JOIN element_types et

                ON e.type_id = et.type_id


                JOIN sections s

                ON e.section_id = s.section_id


                WHERE

                    e.element_id = :id

                    AND s.name = :section

                """
            ),
            {
                "id": element_id,

                "section": section_name
            }

        ).first()



        if not element:

            return HTMLResponse(
                "Element not found",
                status_code=404
            )




        max_position = connection.execute(
            text(
                """
                SELECT COALESCE(MAX(e.position),0)

                FROM elements e

                JOIN sections s

                ON e.section_id = s.section_id


                WHERE s.name=:section

                """
            ),
            {
                "section": section_name
            }

        ).scalar()



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


            "positions": list(
                range(
                    1,
                    max_position + 1
                )
            ),


            "default_position": element.position

        }

    )







@app.post("/admin/{section_name}/{element_id}/edit")
async def admin_edit_element_post(
    section_name: str,
    element_id: int,

    element_type: str = Form(...),
    position: int = Form(...),

    heading: str | None = Form(None),
    subtitle: str | None = Form(None),
    text_value: str | None = Form(None, alias="text"),
    label: str | None = Form(None),
    link: str | None = Form(None),

    image: UploadFile | None = File(None)
):


    config = ADMIN_CONFIG.get(section_name)



    if not config:

        return HTMLResponse(
            "Section configuration not found",
            status_code=404
        )



    if element_type not in config["types"]:

        return HTMLResponse(
            "Invalid type",
            status_code=400
        )
    
    image_base64 = None

    if image and image.filename:

        content = await image.read()

        image_base64 = (
            "data:"
            + image.content_type
            + ";base64,"
            + base64.b64encode(content).decode()
        )





    with engine.begin() as connection:



        old_element = connection.execute(

            text(
                """
                SELECT

                    position,

                    heading,

                    subtitle,

                    text,

                    label,

                    image,

                    link


                FROM elements

                WHERE element_id=:id

                """
            ),

            {
                "id": element_id
            }

        ).first()




        if not old_element:

            return HTMLResponse(
                "Element not found",
                status_code=404
            )





        if heading is None or heading == "":
            heading = old_element.heading



        if subtitle is None or subtitle == "":
            subtitle = old_element.subtitle



        if text_value is None or text_value == "":
            text_value = old_element.text



        if label is None or label == "":
            label = old_element.label



        if link is None or link == "":
            link = old_element.link
        
        if image_base64 is None:
            image_base64 = old_element.image





        old_position = old_element.position





        if old_position != position:


            another = connection.execute(

                text(
                    """
                    SELECT element_id

                    FROM elements

                    WHERE section_id = (

                        SELECT section_id

                        FROM elements

                        WHERE element_id=:id

                    )

                    AND position=:position

                    AND element_id != :id

                    """
                ),

                {

                    "id": element_id,

                    "position": position

                }

            ).first()



            if another:


                connection.execute(

                    text(
                        """
                        UPDATE elements

                        SET position=:old_position

                        WHERE element_id=:another_id

                        """
                    ),

                    {

                        "old_position": old_position,

                        "another_id": another.element_id

                    }

                )







        element_type_row = connection.execute(

            text(
                """
                SELECT type_id

                FROM element_types

                WHERE name=:name

                """
            ),

            {
                "name": element_type
            }

        ).first()






        connection.execute(

            text(
                """
                UPDATE elements


                SET

                    type_id=:type_id,

                    position=:position,

                    heading=:heading,

                    subtitle=:subtitle,

                    text=:text,

                    label=:label,

                    image=:image,

                    link=:link


                WHERE element_id=:id

                """
            ),

            {


                "type_id": element_type_row.type_id,


                "position": position,


                "heading": heading,


                "subtitle": subtitle,


                "text": text_value,


                "label": label,

                "image": image_base64,

                "link": link,


                "id": element_id

            }

        )



    return RedirectResponse(

        url=f"/admin/{section_name}",

        status_code=303

    )

@app.post("/admin/{section_name}/{element_id}/delete")
async def admin_delete_element(
    section_name: str,
    element_id: int
):

    config = ADMIN_CONFIG.get(section_name)

    if not config:
        return HTMLResponse(
            "Section configuration not found",
            status_code=404
        )


    with engine.begin() as connection:

        element = connection.execute(
            text(
                """
                SELECT
                    element_id,
                    section_id,
                    position
                FROM elements
                WHERE element_id=:id
                """
            ),
            {
                "id": element_id
            }
        ).first()


        if not element:
            return HTMLResponse(
                "Element not found",
                status_code=404
            )


        connection.execute(
            text(
                """
                DELETE FROM elements
                WHERE element_id=:id
                """
            ),
            {
                "id": element_id
            }
        )


        connection.execute(
            text(
                """
                UPDATE elements
                SET position = position - 1
                WHERE section_id=:section_id
                AND position > :position
                """
            ),
            {
                "section_id": element.section_id,
                "position": element.position
            }
        )


    return RedirectResponse(
        url=f"/admin/{section_name}",
        status_code=303
    )