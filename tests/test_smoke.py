import requests

from http import HTTPStatus
from pydantic_core import Url
from app.models.User import UserCreate, UserCreateResponse


def test__post_user_should_create_new_user(app_url, delete_user):
    payload = UserCreate()
    response = requests.post(f"{app_url}/api/users/", json=payload.model_dump())
    assert response.status_code == HTTPStatus.CREATED
    new_user = UserCreateResponse.model_validate(response.json())
    assert new_user.last_name == payload.last_name
    delete_user(new_user.id)


def test__delete_user_should_be_deleted(app_url, create_new_user):
    new_user_id = create_new_user.id
    created_user = requests.get(f"{app_url}/api/users/{new_user_id}")
    assert created_user.status_code == HTTPStatus.OK
    response = requests.delete(f"{app_url}/api/users/{new_user_id}")
    assert response.status_code == HTTPStatus.OK
    deleted_user = requests.get(f"{app_url}/api/users/{new_user_id}")
    assert deleted_user.status_code == HTTPStatus.NOT_FOUND


def test__patch_user_should_have_updated_first_name(app_url, create_new_user):
    new_user_id = create_new_user.id
    updated_user_name = 'Test'
    assert create_new_user.first_name != updated_user_name
    # payload = UserUpdate(first_name='Test') С этой строкой выдает ошибку 500, но хотелось бы ее использовать
    payload = {'first_name': updated_user_name}
    response = requests.patch(f"{app_url}/api/users/{new_user_id}", json=payload)
    assert response.status_code == HTTPStatus.OK
    updated_user = requests.get(f"{app_url}/api/users/{new_user_id}")
    updated_name = updated_user.json()['first_name']
    assert updated_name == updated_user_name


def test__patch_user_should_have_updated_last_name(app_url, create_new_user):
    new_user_id = create_new_user.id
    assert create_new_user.last_name != 'Test'
    payload = {'last_name': 'Test'}
    response = requests.patch(f"{app_url}/api/users/{new_user_id}", json=payload)
    assert response.status_code == HTTPStatus.OK
    updated_user = requests.get(f"{app_url}/api/users/{new_user_id}")
    updated_last_name = updated_user.json()['last_name']
    assert updated_last_name == 'Test'


def test__patch_user_should_have_updated_email(app_url, create_new_user):
    new_user_id = create_new_user.id
    new_user_email = create_new_user.email
    updated_user_email = 'test@test.com'
    assert new_user_email != updated_user_email
    payload = {'email': updated_user_email}
    response = requests.patch(f"{app_url}/api/users/{new_user_id}", json=payload)
    assert response.status_code == HTTPStatus.OK
    updated_user = requests.get(f"{app_url}/api/users/{new_user_id}")
    updated_email = updated_user.json()['email']
    assert updated_email == updated_user_email


def test__put_user_should_return_405_error(app_url, create_new_user):
    new_user_id = create_new_user.id
    updated_user_email = 'test@test.com'
    assert create_new_user.email != updated_user_email
    payload = {'email': updated_user_email}
    response = requests.put(f"{app_url}/api/users/{new_user_id}", json=payload)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test__delete_not_existing_user_should_return_404_error(app_url, create_new_user):
    invalid_user_id = create_new_user.id + 1
    response = requests.delete(f"{app_url}/api/users/{invalid_user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test__post_user_full_flow(app_url, delete_user):
    payload = UserCreate()
    response = requests.post(f"{app_url}/api/users/", json=payload.model_dump())
    assert response.status_code == HTTPStatus.CREATED

    new_user = UserCreateResponse.model_validate(response.json())
    assert new_user.last_name == payload.last_name
    assert new_user.first_name == payload.first_name
    assert new_user.email == payload.email
    assert new_user.avatar == Url(payload.avatar)

    updated_first_name = 'John'
    updated_last_name = 'Malcovich'
    updated_email = 'test2@example.com'
    updated_avatar = 'https://www.test.com'
    payload_to_update = {"email": updated_email,
                         "first_name": updated_first_name,
                         "last_name": updated_last_name,
                         "avatar": updated_avatar
                         }
    response = requests.patch(f"{app_url}/api/users/{new_user.id}", json=payload_to_update)
    assert response.status_code == HTTPStatus.OK

    up_user = UserCreateResponse.model_validate(response.json())
    assert up_user.first_name == updated_first_name
    assert up_user.last_name == updated_last_name
    assert up_user.email == updated_email
    assert up_user.avatar == Url(updated_avatar)

    delete_user(new_user.id)
    response = requests.get(f"{app_url}/api/users/{new_user.id}", json=payload.model_dump())
    assert response.status_code == HTTPStatus.NOT_FOUND
