from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch
from src.app import app
from db.seed import seed_db
from datetime import date, timedelta

@pytest.fixture(autouse=True)
@patch("db.seed.EDEXCEL_GCE_DATA", "test/data/test_edexcel_gce.xlsx")
@patch("db.seed.EDEXCEL_GCSE_DATA", "test/data/test_edexcel_gcse.xlsx")
def seed_database():
    seed_db()

@pytest.fixture
def test_client():
    return TestClient(app)

class TestHealthcheck:
    @pytest.mark.it('Check connects to server')
    def test_connects_to_server(self, test_client):
        result = test_client.get('/')
        assert result.status_code == 200
        assert result.json() == {"message": 'Everything OK'}
    
class TestGetExam:
    @pytest.mark.it('Returns 200 status code')
    def test_200_status_code(self, test_client):
        result = test_client.get('exam/TEST/01')
        assert result.status_code == 200

    @pytest.mark.it('Returns expected data')
    def test_returns_data(self, test_client):
        expected = {
            'syllabus_code': 'TEST',
            'component_code': '01',
            'board': 'Pearson',
            'subject': 'GCSE Test',
            'title': 'Test Exam 1',
            'date': '2025-05-22',
            'time': 'PM',
            'duration': 2100,

        }
        result = test_client.get('/exam/TEST/01')
        assert result.json() == expected
    
    @pytest.mark.skip
    @pytest.mark.it('Returns 404 if data not in database')
    def test_404_if_data_not_found(self, test_client):
        result = test_client.get('/exam/missing/01')
        assert result.status_code == 404