from fastapi import FastAPI
from db.connection import connect_to_db

app = FastAPI()

@app.get('/')
def healthcheck():
    return {"message": 'Everything OK'}


@app.get('/exams')
def get_exams():
    pass


@app.get('/exam/{syllabus}')
def get_syllabus_exams(syllabus: str):
    pass


@app.get('/exam/{syllabus}/{component}')
def get_exam(syllabus: str, component: str):
    return {"message": 'Everything OK'}
