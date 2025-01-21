import pytest
from pg8000.native import Connection
from db.connection import connect_to_db


@pytest.mark.it('Check that connect to db returns database connection')
def test_returns_db_connection():
    db = None
    try:
        db = connect_to_db()
        assert isinstance(db, Connection)
    finally:
        if db:
            db.close()
