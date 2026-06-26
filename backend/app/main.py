from pathlib import Path
import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()


BASE_DIR = Path(__file__).resolve().parent.parent.parent

templates = Jinja2Templates(
    directory=str(BASE_DIR / "frontend/templates")
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    with open(
        BASE_DIR / "json/struct_json.json",
        encoding="utf-8"
    ) as file:
        data = json.load(file)

    print(data.keys())

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "data": data
        }
    )