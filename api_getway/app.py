# backend/service3/app.py
from fastapi import FastAPI

app = FastAPI(title="Управление данными", version="1.0.0")

# Можно реализовать CRUD по другим моделям или административные операции
# Для примера — пустой API