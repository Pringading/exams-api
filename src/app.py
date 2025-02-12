from fastapi import FastAPI
from db.connection import connect_to_db
from schemas.response import Exam

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
    query = """
    SELECT * FROM exams 
    WHERE component_code = :comp 
        AND syllabus_code = :syll;"""
    db = None
    try:
        db = connect_to_db()
        data = db.run(query, comp=component, syll=syllabus)
        cols = [col['name'] for col in db.columns]
        result = dict(zip(cols, data[0]))
        return result
    finally:
        if db:
            db.close()
