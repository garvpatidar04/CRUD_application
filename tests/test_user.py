import pytest
from app import schemas
import jwt
from app.config import settings

# test for user
@pytest.mark.parametrize("email, password, status_code", [
    ("snds@gmail.com", "2f54ff", 201),
    ("gghh4.scc@gmail.com", "23nj5", 201)
])
def test_user_create(client, email, password, status_code):
    """
    test for user_create api method"""
    res = client.post('/users/', json={'email': email, 'password': password})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == email
    assert res.status_code == status_code


def test_user_login(client, test_user):
# def test_user_login(client):
    """
    test for login api method"""
    res = client.post(
        '/login', data={'username': test_user['email'], 'password': test_user['password']})
    login_res = schemas.Token(**res.json())
    decoded_res = jwt.decode(
        login_res.token, key=settings.secret_key, algorithms=settings.algorithm)
    assert decoded_res['user_id'] == test_user['id']
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("username, password, status_code", [
    ('test@gmail.com', 'afafaqf3', 403),
    ('2342@gmail.com', 'test123', 403),
    ('2342@gmail.com', 'afafaqf3', 403),
    (None, 'afafaqf3', 422),
    ('2342@gmail.com', None, 422),
])
def test_invalid_login(client, test_user, username, password, status_code):
# def test_user_login(client):
    """
    test for login api method but invalid login"""
    res = client.post(
        '/login', data={'username': username, 'password': password})

    assert res.status_code == status_code

def test_single_user(client, test_user):
    res = client.get(f'/users/{test_user["id"]}')

    assert res.json().get('email') == test_user['email']
    assert res.status_code == 200