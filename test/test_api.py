from fastapi.testclient import TestClient
import pytest
from src.app import app
from db.seed import seed_db

@pytest.fixture
def seed_database(autouse=True):
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
        result = test_client.get('exam/hello/there')
        assert result.status_code == 200

    @pytest.mark.skip
    @pytest.mark.it('Returns expected data')
    def test_returns_data(self, test_client):
        expected = {
            "Exam"
        }
        result = test_client.get('/exam/TEST/01')
    
    @pytest.mark.skip
    @pytest.mark.it('Returns expected data')
    def test_404_if_data_not_found(self, test_client):
        result = test_client.get('/exam/missing/01')
        assert result.status_code == 404