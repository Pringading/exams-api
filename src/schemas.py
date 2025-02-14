from pydantic import BaseModel
from datetime import date, timedelta


class Exam(BaseModel):
    syllabus_code: str
    component_code: str
    board: str
    subject: str
    title: str
    date: date
    time: str | None
    duration: timedelta
