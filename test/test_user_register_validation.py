

def test_user_registration_missing_first_name(client_empty_db):
    data = {

        "last_name": "Mutavdzic",
        "email": "marko.mutavdzic@factoryww.com",
        "username": "mare",
        "password": "0147"
    }

    url = '/user_registration'

    response = client_empty_db.post(url, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'first_name': ['Missing data for required field.']}


def test_user_registration_first_name_too_long(client_empty_db):
    data = {
        "first_name": "Marko" * 11,
        "last_name": "Mutavdzic",
        "email": "marko.mutavdzic@factoryww.com",
        "username": "mare1",
        "password": "0147"
    }

    url = '/user_registration'

    response = client_empty_db.post(url, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'first_name': ['Longer than maximum length 50.']}


def test_user_registration_missing_last_name(client_empty_db):
    data = {
        "first_name": "Marko",

        "email": "marko.mutavdzic@factoryww.com",
        "username": "mare1",
        "password": "0147"
    }

    url = '/user_registration'

    response = client_empty_db.post(url, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'last_name': ['Missing data for required field.']}


def test_user_registration_last_name_too_long(client_empty_db):
    data = {
        "first_name": "Marko",
        "last_name": "Mutavdzic"*10,
        "email": "marko.mutavdzic@factoryww.com",
        "username": "mare1",
        "password": "0147"
    }

    url = '/user_registration'

    response = client_empty_db.post(url, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'last_name': ['Longer than maximum length 50.']}


def test_user_registration_missing_email(client_empty_db):
    data = {
        "first_name": "Marko",
        "last_name": "Mutavdzic",

        "username": "mare",
        "password": "0147"
    }

    url = '/user_registration'

    response = client_empty_db.post(url, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'email': ['Missing data for required field.']}


def test_user_registration_email_too_long(client_empty_db):
    data = {
        "first_name": "Marko",
        "last_name": "Mutavdzic",
        "email": "marko.mutavdzic@factoryww.com"*2,
        "username": "mare",
        "password": "0147"
    }

    url = '/user_registration'

    response = client_empty_db.post(url, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'email': ['Longer than maximum length 50.']}


def test_user_registration_missing_username(client_empty_db):
    data = {
        "first_name": "Marko",
        "last_name": "Mutavdzic",
        "email": "marko.mutavdzic@factoryww.com",

        "password": "0147"
    }

    url = '/user_registration'

    response = client_empty_db.post(url, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'username': ['Missing data for required field.']}


def test_user_registration_username_too_long(client_empty_db):
    data = {
        "first_name": "Marko",
        "last_name": "Mutavdzic",
        "email": "marko.mutavdzic@factoryww.com",
        "username": "mare"*15,
        "password": "0147"
    }

    url = '/user_registration'

    response = client_empty_db.post(url, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'username': ['Longer than maximum length 50.']}


def test_user_registration_missing_password(client_empty_db):
    data = {
        "first_name": "Marko",
        "last_name": "Mutavdzic",
        "email": "marko.mutavdzic@factoryww.com",
        "username": "mare"

    }

    url = '/user_registration'

    response = client_empty_db.post(url, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'password': ['Missing data for required field.']}


def test_user_registration_password_too_long(client_empty_db):
    data = {
        "first_name": "Marko",
        "last_name": "Mutavdzic",
        "email": "marko.mutavdzic@factoryww.com",
        "username": "mare",
        "password": "0147" * 15
    }

    url = '/user_registration'

    response = client_empty_db.post(url, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'password': ['Longer than maximum length 50.']}
