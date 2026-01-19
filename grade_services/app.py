# backend/service2/app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Расписание и оценки", version="1.0.0")


class Schedule(BaseModel):
    id: str
    course_name: str
    schedule_time: str
    location: str


class Grade(BaseModel):
    course_name: str
    student_id: str
    grade_value: str
    date_awarded: str


# Пример данных
schedules = [
    Schedule(id="1", course_name="Математика", schedule_time="2023-10-01T09:00", location="Аудитория 101"),
    Schedule(id="2", course_name="История", schedule_time="2023-10-02T11:00", location="Аудитория 102"),
]

grades = [
    Grade(course_name="Математика", student_id="123", grade_value="A", date_awarded="2023-09-30"),
    Grade(course_name="История", student_id="123", grade_value="B+", date_awarded="2023-09-25"),
]


@app.get("//schedule", response_model=List[Schedule], tags=["Расписание и оценки"])
async def get_schedule():
    return schedules


@app.get("//grades", response_model=List[Grade], tags=["Расписание и оценки"])
async def get_grades():
    return grades