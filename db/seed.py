from pg8000.native import Connection
from db.connection import connect_to_db


def seed_db() -> None:
    """seed database with 
    
    sklfj"""

    pass


def create_exams_table(db: Connection) -> None:
    """creates exam table to the database provided(db)"""

    db.run("""
        CREATE TABLE exams (
           syllabus_code VARCHAR(6) NOT NULL,
           component_code VARCHAR(4),
           board VARCHAR(20) NOT NULL,
           subject VARCHAR(40),
           title VARCHAR(60),
           date DATE,
           time CHAR(2),
           duration INTERVAL,
           PRIMARY KEY(syllabus_code, component_code)
        );
    """)


def drop_exams_table(db: Connection) -> None:
    db.run("DROP TABLE IF EXISTS exams;")