import pytest
from pg8000.native import Connection
from db.connection import connect_to_db
from db.seed import (
    seed_db, create_exams_table, drop_exams_table
)


class TestConnection:
    """Testing connect_to_db function in db/connection.py"""
    @pytest.mark.it('Check that connect to db returns database connection')
    def test_returns_db_connection(self):
        """Tests that connect_to_db returns a Connection object and 
        then closes the connection inside a finally block"""

        db = None
        try:
            db = connect_to_db()
            assert isinstance(db, Connection)
        finally:
            if db:
                db.close()


class TestCreateDropExamsTable:
    """Testing the functions that create and drop the exams table within 
    db/seed.py"""

    @pytest.fixture(scope='function')
    def db_connection(self):
        """Pytest fixture that yields a databse connection
        
        Includes finally clause to ensure that the connection is closed even
        if the test encounters an error."""

        db = None
        try:
            db = connect_to_db()
            yield db
        finally:
            if db:
                # remove exams table before closing the connection.
                db.run('DROP TABLE IF EXISTS exams;')
                db.close()


    @pytest.mark.it('Create adds exams table to the database')
    def test_exams_table_created(self, db_connection):
        create_exams_table(db_connection)

        # gets list of public tables in the database, (should only be 1).
        result = db_connection.run(
            """SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';"""
        )
        assert result == [['exams']]
    

    @pytest.mark.it('Exams timetable has the expected columns')
    def test_exams_timetable_has_expected_columns(self, db_connection):
        expected_columns = [
            'syllabus_code',
            'component_code',
            'board',
            'subject',
            'title',
            'date',
            'time',
            'duration'
        ]
        create_exams_table(db_connection)
        result = db_connection.run(
            """SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'exams';"""
        )
        for column in expected_columns:
            assert [column] in result
        assert len(result) == len(expected_columns)
    
    # test primary key

