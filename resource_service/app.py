# backend/service1/app.py
from fastapi import FastAPI, HTTPException, Path, Query, Body
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

app = FastAPI(title="API для учебных ресурсов", version="1.0.0")


class Resource(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    url: HttpUrl
    author: str
    date_published: str
    content_type: str
    discipline: str
    level: str
    tags: List[str] = []


# Временное "база данных"
resources_db = {
    "1": Resource(
        id="1",
        title="Алгебраические алгоритмы",
        description="Обзор методов алгебраических алгоритмов для решений уравнений",
        url="https://example.com/algorithms",
        author="Иван Иванов",
        date_published="2023-09-15",
        content_type="учебник",
        discipline="Математика",
        level="Базовый",
        tags=["алгебра", "алгоритмы"]
    ),
    "2": Resource(
        id="2",
        title="Введение в программирование",
        description="Курс для начинающих по основам программирования",
        url="https://example.com/python-introduction",
        author="Петр Петров",
        date_published="2023-10-01",
        content_type="видео",
        discipline="Информатика",
        level="Начинающий",
        tags=["программирование", "Python"]
    ),
    "3": Resource(
        id="3",
        title="История российской архитектуры",
        description="Статья об эволюции русской архитектуры XVIII-XIX веков",
        url="https://example.com/russian-architecture",
        author="Мария Смирнова",
        date_published="2022-12-10",
        content_type="статья",
        discipline="История",
        level="Средний",
        tags=["история", "архитектура"]
    )
}


@app.get("//resources", response_model=List[Resource], tags=["Учебные материалы"])
async def get_resources(
    discipline: Optional[str] = Query(None),
    level: Optional[str] = Query(None),
    content_type: Optional[str] = Query(None),
):
    results = list(resources_db.values())
    if discipline:
        results = [r for r in results if r.discipline == discipline]
    if level:
        results = [r for r in results if r.level == level]
    if content_type:
        results = [r for r in results if r.content_type == content_type]
    print(results)
    return results


@app.get("/resources/{id}", response_model=Resource, tags=["Учебные материалы"])
async def get_resource(id: str = Path(...)):
    resource = resources_db.get(id)
    if not resource:
        raise HTTPException(404, detail="Ресурс не найден")
    return resource


@app.post("/admin/resources", response_model=None, status_code=201, tags=["Управление данными"])
async def create_resource(resource: Resource = Body(...)):
    if resource.id in resources_db:
        raise HTTPException(400, detail="Ресурс с таким ID уже существует")
    resources_db[resource.id] = resource
    return


@app.put("/admin/resources/{id}", response_model=None, tags=["Управление данными"])
async def update_resource(id: str = Path(...), resource: Resource = Body(...)):
    if id not in resources_db:
        raise HTTPException(404, detail="Ресурс не найден")
    resources_db[id] = resource
    return


@app.delete("/admin/resources/{id}", response_model=None, status_code=204, tags=["Управление данными"])
async def delete_resource(id: str = Path(...)):
    if id not in resources_db:
        raise HTTPException(404, detail="Ресурс не найден")
    del resources_db[id]
    return