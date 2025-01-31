import pytest
import pandas as pd
from unittest.mock import patch
from pg8000.native import Connection
from db.connection import connect_to_db
from db.seed import (
    seed_db, create_exams_table, drop_exams_table,
    extract_headings_from_df, df_to_string, insert_data_into_exams_table
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
            db.run('DROP TABLE IF EXISTS exams;')
            yield db
        finally:
            if db:
                # remove exams table before closing the connection.
                db.run('DROP TABLE IF EXISTS exams;')
                db.close()


    @pytest.mark.it('Create adds exams table to the database')
    def test_exams_table_created(self, db_connection):
        create_exams_table(db_connection)

        # gets list of public tables in the database.
        result = db_connection.run(
            """SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';"""
        )
        assert ['exams'] in result
    

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

        # gets list of columns in the exams table
        result = db_connection.run(
            """SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'exams';"""
        )
        for column in expected_columns:
            assert [column] in result
        assert len(result) == len(expected_columns)

    @pytest.mark.it('Test drop exams table removes the exams table')
    def test_drop_exams_table_removes_table(self, db_connection):
        create_exams_table(db_connection)
        drop_exams_table(db_connection)
        
        # gets list of public tables in the database, (should only be 1).
        result = db_connection.run(
            """SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';"""
        )

        assert ['exams'] not in result


class TestInsertDataFuncs:
    """Testing extract_headings_from_df, df_to_string and 
    insert_data_into_exams_table functions from db/seed.py"""

    @pytest.mark.it('Extracts headings from dataframe to comma separated string.')
    def test_extracts_headings(self):
        test_df = pd.DataFrame({"heading1": [1], "heading2":[2]})
        assert extract_headings_from_df(test_df) == 'heading1, heading2'

    @pytest.mark.it('Transforms data form dataframe to a comma separated string')
    def test_extracts_data(self):
        expected = "('1', '2', '3'), ('2', '3', '4')"
        test_df = pd.DataFrame({"h1": [1, 2], "h2": [2, 3], "h3": [3, 4]})
        assert df_to_string(test_df) == expected

    @pytest.mark.it('insert data function adds data to the exams table')
    def test_adds_data_to_table(self):
        test_df = pd.DataFrame({
            "syllabus_code": ["syll"],
            "component_code": ["comp"],
            "date": ["01-01-01"],
            "board": ["Pearson"],
            "subject": ["Subject1"],
            "title": ["title1"],
            "time": ["AM"],
            "duration": ["01h 30m"]
        })
        expected = [
            'syll', 
            'comp', 
            'Pearson', 
            'Subject1', 
            'title1', 
            '2001-01-01',
            'AM', 
            '1:30:00'
        ]
        db = None
        try: 
            db = connect_to_db()
            drop_exams_table(db)
            create_exams_table(db)
            insert_data_into_exams_table(db, test_df)
            result = db.run('SELECT * FROM exams;')
            drop_exams_table(db)
            print(result)
            assert [str(value) for value in result[0]] == expected
        finally:
            if db:
                db.close()
        

class TestSeedDB:
    """Testing seed_db function from db/seed.py"""

    @pytest.mark.it('Seed DB adds expected data to database.')
    @patch('db.seed.EDEXCEL_GCSE_DATA', 'test/data/test_edexcel_gcse.xlsx')
    @patch('db.seed.EDEXCEL_GCE_DATA', 'test/data/test_edexcel_gce.xlsx')
    def test_seed_db(self):
        """Testing seed function inserts expected data into databse.
        
        Uses patching to get data from test/data/ folder. Uses finally block
        to ensure database connection is closed"""
        
        expected = [
            'TEST', 
            '01', 
            'Pearson', 
            'GCSE Test', 
            'Test Exam 1', 
            '2025-05-22', 
            'PM', 
            '0:35:00'
        ]
        db = None
        seed_db()
        try: 
            db = connect_to_db()
            result = db.run('SELECT * FROM exams;')
            drop_exams_table(db)
            print(result[0])
            assert [str(value) for value in result[0]] == expected
            assert len(result) == 6
        finally:
            if db:
                db.close()
