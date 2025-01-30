from pg8000.native import Connection, literal, identifier
import pandas as pd
from db.connection import connect_to_db
from db.utils.edexcel_data import (
    edexcel_data_to_df, 
    EDEXCEL_GCE_DATA, 
    EDEXCEL_GCSE_DATA
)


def seed_db() -> None:
    """Add exams table and data to database.
    
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


def extract_headings_from_df(df: pd.DataFrame) -> str:
    """Extracts headings from given dataframe.
    
    Args:
        df: pandas dataframe
    Returns comma separated string of headings."""
    
    return ", ".join(identifier(heading) for heading in df.columns)


def df_to_string(df: pd.DataFrame) -> str:
    """Converts each row in dataframe to a comma separated string.

    Each row is surrounded by brackets and separated by a comma to be used in
    a SQL INSERT query. Uses pg8000 literal function to prevent SQL injection.

    Example:
    Input:
        | 1 | 2 | 3 |
        | 2 | 3 | 4 |
    Output:
        "('1', '2', '3'), ('2', '3', '4')"
    """
    row_strings = []
    for row in df.values:
        string = ", ".join(literal(value) for value in row)
        print(string)
        row_strings.append("(" + string + ")")
    return ", ".join(row_strings)


def insert_data_into_exams_table(db: Connection, df: pd.DataFrame) -> None:
    """Inserts data from a dataframe into exams table.
    
    Args:
        db: pg8000 connection to database.
        df: pandas dataframe
    Returns None
    """
    
    pass

def drop_exams_table(db: Connection) -> None:
    db.run("DROP TABLE IF EXISTS exams;")