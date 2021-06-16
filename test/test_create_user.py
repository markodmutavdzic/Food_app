

def test_user_registration_full(client_empty_db):
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