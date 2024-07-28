import requests

from http import HTTPStatus
from app.models.User import UserCreate, UserCreateResponse


def test__post_user_should_create_new_user(app_url, delete_user):
    payload = UserCreate()
    response = requests.post(f"{app_url}/api/users/", json=payload.model_dump())
    assert response.status_code == HTTPStatus.CREATED
    new_client = response.json()
    new_user = UserCreateResponse(**new_client)
    user_last_name = new_user.last_name
    assert user_last_name == payload.last_name
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
    new_user_name = create_new_user.first_name
    updated_user_name = 'Test'
    assert new_user_name != updated_user_name
    # payload = UserUpdate(first_name='Test') С этой строкой выдает ошибку 500, но хотелось бы ее использовать
    payload = {'first_name': updated_user_name}
    response = requests.patch(f"{app_url}/api/users/{new_user_id}", json=payload)
    assert response.status_code == HTTPStatus.OK
    updated_user = requests.get(f"{app_url}/api/users/{new_user_id}")
    updated_name = updated_user.json()['first_name']
    assert updated_name == updated_user_name


def test__patch_user_should_have_updated_last_name(app_url, create_new_user):
    new_user_id = create_new_user.id
    new_user_last_name = create_new_user.last_name
    assert new_user_last_name != 'Test'
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
    new_user_email = create_new_user.email
    updated_user_email = 'test@test.com'
    assert new_user_email != updated_user_email
    payload = {'email': updated_user_email}
    response = requests.put(f"{app_url}/api/users/{new_user_id}", json=payload)
    assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED


def test__delete_not_existing_user_should_return(app_url, create_new_user):
    new_user_id = create_new_user.id
    invalid_user_id = new_user_id + 1
    response = requests.delete(f"{app_url}/api/users/{invalid_user_id}")
    assert response.status_code == HTTPStatus.NOT_FOUND
