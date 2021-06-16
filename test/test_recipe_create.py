
from freezegun import freeze_time


@freeze_time('2021-06-16 07:43:06.284695')
def test_recipe_create(client_one_user_db):
    data = {
        "name": "Bread",
        "text": "Mix water, flour and egg",
        "ingredients": "water, flour, egg"
    }
    url = '/recipe_create'
    header = {
        'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzODMwOTMzfQ"
                        ".z2O6YMEHnXD6l0vhfNNBoZS22_r33HGjtXCYBJ-5chE"}
    response = client_one_user_db.post(url, headers=header, json=data)

    assert response.status_code == 200
    assert response.get_json() == {'message': 'New recipe created.'}


@freeze_time('2021-06-16 07:43:06.284695')
def test_recipe_create_missing_name(client_one_user_db):
    data = {

        "text": "Mix water, flour and egg",
        "ingredients": "water, flour, egg"
    }
    url = '/recipe_create'
    header = {
        'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzODMwOTMzfQ"
                        ".z2O6YMEHnXD6l0vhfNNBoZS22_r33HGjtXCYBJ-5chE"}
    response = client_one_user_db.post(url, headers=header, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'name': ['Missing data for required field.']}


@freeze_time('2021-06-16 07:43:06.284695')
def test_recipe_create_name_too_long(client_one_user_db):
    data = {
        "name": "Bread"*12,
        "text": "Mix water, flour and egg",
        "ingredients": "water, flour, egg"
    }
    url = '/recipe_create'
    header = {
        'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzODMwOTMzfQ"
                        ".z2O6YMEHnXD6l0vhfNNBoZS22_r33HGjtXCYBJ-5chE"}
    response = client_one_user_db.post(url, headers=header, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'name': ['Longer than maximum length 50.']}


@freeze_time('2021-06-16 07:43:06.284695')
def test_recipe_create_missing_text(client_one_user_db):
    data = {
        "name": "Bread",

        "ingredients": "water, flour, egg"
    }
    url = '/recipe_create'
    header = {
        'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzODMwOTMzfQ"
                        ".z2O6YMEHnXD6l0vhfNNBoZS22_r33HGjtXCYBJ-5chE"}
    response = client_one_user_db.post(url, headers=header, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'text': ['Missing data for required field.']}


@freeze_time('2021-06-16 07:43:06.284695')
def test_recipe_create_missing_ingredients(client_one_user_db):
    data = {
        "name": "Bread",
        "text": "Mix water, flour and egg",

    }
    url = '/recipe_create'
    header = {
        'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzODMwOTMzfQ"
                        ".z2O6YMEHnXD6l0vhfNNBoZS22_r33HGjtXCYBJ-5chE"}
    response = client_one_user_db.post(url, headers=header, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'ingredients': ['Missing data for required field.']}
