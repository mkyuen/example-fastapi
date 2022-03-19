
from fastapi.testclient import TestClient
from jose import jwt
from app.main import app
from app.routers import post
from app import schemas
from app.oauth2 import SECRET_KEY, ALGORITHM
import pytest


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == 'Welcome to my API'
    assert res.status_code == 200


def test_create_post(client):
    res = client.post("/posts/", json={"title": "Test Create Post 1", "Content": "Create Post 1"})
    print (res.json())
    assert res.status_code == 401


def test_login(client):
    res = client.post(
        "/login", data={"username": "abc@gmail.com", "password": "password"})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, SECRET_KEY, algorithms = [ALGORITHM])
    id = payload.get("user_id")
    print(f"id = {id}")
    print (f"token type = {login_res.token_type}")
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


def test_get_all_posts(authorized_client, test_user):
    res = authorized_client.get("/posts/")
    print(f'test_all_posts: res = {res.json()}')
    assert res.status_code == 200


def test_unauthorized_get_all_posts(client, test_user):
    res = client.get("/posts/")
    print(f'test_unauthorized_all_posts: res = {res.json()}')
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_user):
    res = authorized_client.get(f"/posts/8888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_user):
    res = authorized_client.get(f"/posts/1")
    post = res.json()
    print(f"post id = {post['id']}")
    print(f"post title = {post['title']}")
    print(f"post content = {post['content']}")
    assert post['id'] == 1
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new title", True),
    ("favorite pizza", "i love peperoni", False),
])
def test_create_one_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    #print(f"created post: title = {created_post.title}")
    assert created_post.title == title
    assert res.status_code == 201


def test_unauthorized_create_post(client, test_user):
    res = client.post("/posts/", json={"title": "default title", "content": "default content", "published": False})
    assert res.status_code == 401


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": True
    }
    res = authorized_client.put(f"/posts/1", json=data)
    updated_post = schemas.Post(**res.json())
    print(f"updated_post {updated_post.title}")
    assert res.status_code == 200


def test_unauthorized_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "published": True
    }
    res = client.put(f"/posts/1", json=data)
    assert res.status_code == 401


def test_unauthorized_delete_post(client, test_user):
    res = client.delete("/posts/1")
    assert res.status_code == 401


def test_delete_one_post(authorized_client, test_user):
    res = authorized_client.delete("/posts/1")
    assert res.status_code == 204


def test_delete_one_post_non_exist(authorized_client, test_user):
    res = authorized_client.delete("/posts/8888")
    assert res.status_code == 404


