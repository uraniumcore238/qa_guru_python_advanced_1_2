import json
import os
from http import HTTPStatus

import tests
from pathlib import Path

import dotenv
import pytest
import requests

from app.models.User import UserCreate, UserCreateResponse


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture(scope="module")
def fill_test_data(app_url):
    users_file = str(Path(tests.__file__).parent.parent.joinpath('users.json'))
    with open(users_file) as f:
        test_data_users = json.load(f)
    api_users = []
    for user in test_data_users:
        response = requests.post(f"{app_url}/api/users/", json=user)
        api_users.append(response.json())
    user_ids = [user["id"] for user in api_users]

    yield user_ids

    for user_id in user_ids:
        requests.delete(f"{app_url}/api/users/{user_id}")


@pytest.fixture
def users(app_url):
    response = requests.get(f"{app_url}/api/users/")
    assert response.status_code == HTTPStatus.OK
    return response.json()


@pytest.fixture()
def create_new_user(app_url):
    payload = UserCreate()
    response = requests.post(f"{app_url}/api/users/", json=payload.model_dump())
    assert response.status_code == HTTPStatus.CREATED
    user = UserCreateResponse.model_validate(response.json())

    yield user
    requests.delete(f"{app_url}/api/users/{user.id}")


@pytest.fixture
def delete_user(app_url):
    def _delete_user(user_id):
        response = requests.delete(f"{app_url}/api/users/{user_id}")
        assert response.status_code == HTTPStatus.OK
        return response

    return _delete_user
