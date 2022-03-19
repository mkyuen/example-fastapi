
from fastapi.testclient import TestClient
from app.main import app
from app.oauth2 import create_access_token
import pytest

@pytest.fixture
def test_user():
    return {"id": "user_id_1"}

#@pytest.fixture
#def test_posts():
#    return [
#            {"id": 1, "title": "title 1", "content": "content 1", "published": True},
#            {"id": 2, "title": "title 2", "content": "content 2", "published": True},
#        ]

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client
