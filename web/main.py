from fastapi import FastAPI
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from web.app.routers.health import router as health_router
from web.app.routers.exercises import router as exercises_router
from web.app.services.exercise_catalog import (
    get_exercise_groups,
    CATEGORY_TITLES,
    get_ordered_category_cards,
)

app = FastAPI()

# Static files
BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(directory=BASE_DIR / "templates")

app.include_router(health_router)
app.include_router(exercises_router)


@app.get("/")
def index(request: Request):
    exercise_groups = get_exercise_groups()
    category_cards = get_ordered_category_cards(exercise_groups)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "exercise_groups": exercise_groups,
            "category_cards": category_cards,
            "category_titles": CATEGORY_TITLES,
            "problem_description": None,
            "view": "home",
        },
    )

@app.get("/favicon.ico")
def favicon():
    return FileResponse(
        BASE_DIR / "static" / "favicon.ico"
    )
