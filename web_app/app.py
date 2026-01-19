# web_app/app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI()

# подключение шаблонов
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


API_BASE_URLS = {
    "resources": "http://localhost:8001/",
    "schedule": "http://localhost:8002/",
}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/resources", response_class=HTMLResponse)
async def resources_page(request: Request):
    async with httpx.AsyncClient() as client:
        res = await client.get(API_BASE_URLS["resources"] + "/resources")
        resources = res.json()
    return templates.TemplateResponse("resources.html", {"request": request, "resources": resources})


@app.get("/schedule", response_class=HTMLResponse)
async def schedule_page(request: Request):
    async with httpx.AsyncClient() as client:
        res = await client.get(API_BASE_URLS["schedule"] + "/schedule")
        schedule_list = res.json()
    return templates.TemplateResponse("schedule.html", {"request": request, "schedule": schedule_list})
