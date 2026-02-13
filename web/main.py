from fastapi import FastAPI
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from web.app.routers.health import router as health_router
from web.app.routers.exercises import router as exercises_router

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
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )

@app.get("/favicon.ico")
def favicon():
    return FileResponse(
        BASE_DIR / "static" / "favicon.ico"
    )
