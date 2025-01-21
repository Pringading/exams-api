from pg8000.native import Connection
from db.connection import connect_to_db


def seed_db() -> None:
    """seed database with 
    
    sklfj"""

    pass

def create_exams_table(db: Connection) -> None:
    db.run("""CREATE TABLE exams (name INT);""")

def drop_exams_table(db: Connection) -> None:
    pass