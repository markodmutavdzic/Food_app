

def test_user_registration_valid_email(client_empty_db, patch_clearbit):
    data = {
        "first_name": "Marko",
        "last_name": "Mutavdzic",
        "email": "marko.mutavdzic@factoryww.com",
        "username": "mare",
        "password": "0147"
    }

    url = '/user_registration'

    response = client_empty_db.post(url, json=data)

    assert response.status_code == 200
    assert response.get_json() == {'message': 'New user created.'}


def test_user_registration_invalid_email(client_empty_db):
    data = {
        "first_name": "Marko",
        "last_name": "Mutavdzic",
        "email": "marko.mutavdzic@factory.com",
        "username": "mare",
        "password": "0147"
    }

    url = '/user_registration'

    response = client_empty_db.post(url, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'message': 'Invalid email'}