from fastapi import FastAPI
from db.connection import connect_to_db
from src.schemas import Exam
from src.helpers import data_to_dict_list

app = FastAPI()


@app.get('/')
def healthcheck():
    return {"message": 'Everything OK'}


@app.get('/exams', response_model=list[Exam])
def get_exams():
    """Gets information about all exams"""

    query = "SELECT * FROM exams;"
    db = None
    try:
        db = connect_to_db()
        data = db.run(query)
        result = data_to_dict_list(data, db.columns)
        return result
    finally:
        if db:
            db.close()


@app.get('/exam/{syllabus}/{component}', response_model=Exam)
def get_exam(syllabus: str, component: str):
    """Gets information about one exam."""

    query = """
    SELECT * FROM exams
    WHERE component_code = :comp
        AND syllabus_code = :syll;"""
    db = None
    try:
        db = connect_to_db()
        data = db.run(query, comp=component, syll=syllabus)
        result = data_to_dict_list(data, db.columns)
        return result[0]
    finally:
        if db:
            db.close()
