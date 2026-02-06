from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from web.app.routers.health import router as health_router
from web.app.routers.exercises import router as exercises_router

app = FastAPI()

templates = Jinja2Templates(directory="web/templates")

app.include_router(health_router)
app.include_router(exercises_router)


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )
