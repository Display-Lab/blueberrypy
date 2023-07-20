from fastapi.testclient import TestClient
import pytest

from blueberrypy.main import app

client = TestClient(app)


@pytest.mark.skip()
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello world!"}
