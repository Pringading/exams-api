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
    pass
    # returns exam