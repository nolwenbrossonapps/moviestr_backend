import requests
import pytest


@pytest.mark.dependency()
def test_post_signup():
    data = dict(email="newuser@yopmail.com", password="password", name="Johny")
    r = requests.post("http://127.0.0.1:5000/signup", data=data)
    assert r.status_code in [200, 409]


@pytest.mark.dependency(depends=["test_post_signup"])
def test_post_login():
    data = dict(email="newuser@yopmail.com", password="password", name="Johny")
    r = requests.post("http://127.0.0.1:5000/login", data=data)
    assert r.status_code == 200


@pytest.mark.dependency(depends=["test_post_login"])
def test_token_remove():
    r = requests.post("http://127.0.0.1:5000/token/remove")
    assert r.status_code == 200


def test_logout():
    r = requests.post("http://127.0.0.1:5000/token", json={"email": "newuser@yopmail.com", "password": "password"})
    refresh_token = r.cookies["csrf_refresh_token"]
    access_token = r.cookies["csrf_access_token"]
    refresh_cookie = r.cookies["refresh_token_cookie"]
    access_cookie = r.cookies["access_token_cookie"]
    cookies = {
        "access_token_cookie": access_cookie, 
        "refresh_token_cookie": refresh_cookie,
        "csrf_refresh_token": refresh_token,
        "csrf_access_token": access_token
        }
    new_r = requests.post("http://127.0.0.1:5000/logout", 
                         headers={"X-CSRF-TOKEN-ACCESS": access_token,"X-CSRF-TOKEN-REFRESH": refresh_token},
                         cookies=cookies)
    assert r.status_code == 200
    assert new_r.status_code == 200


def test_access_token_refresh():
    r = requests.post("http://127.0.0.1:5000/token", json={"email": "newuser@yopmail.com", "password": "password"})
    refresh_token = r.cookies["csrf_refresh_token"]
    refresh_cookie = r.cookies["refresh_token_cookie"]
    cookies = {
        "refresh_token_cookie": refresh_cookie,
        "csrf_refresh_token": refresh_token
        }
    new_r = requests.post("http://127.0.0.1:5000/token/access", 
                         headers={"X-CSRF-TOKEN-REFRESH": refresh_token},
                         cookies=cookies)
    assert r.status_code == 200
    assert new_r.status_code == 200


def test_token_validity():
    r = requests.post("http://127.0.0.1:5000/token", json={"email": "newuser@yopmail.com", "password": "password"})
    refresh_token = r.cookies["csrf_refresh_token"]
    access_token = r.cookies["csrf_access_token"]
    refresh_cookie = r.cookies["refresh_token_cookie"]
    access_cookie = r.cookies["access_token_cookie"]
    cookies = {
        "access_token_cookie": access_cookie, 
        "refresh_token_cookie": refresh_cookie,
        "csrf_refresh_token": refresh_token,
        "csrf_access_token": access_token
        }
    new_r = requests.get("http://127.0.0.1:5000/tokens_validity", 
                         cookies=cookies)
    assert r.status_code == 200
    assert new_r.status_code == 200