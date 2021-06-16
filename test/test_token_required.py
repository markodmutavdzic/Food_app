

def test_missing_toket(client_empty_db):

    url = '/recipe_create'
    response = client_empty_db.post(url)

    assert response.status_code == 401
    assert response.get_json() == {'message': 'Token is missing'}


def test_invalid_toket(client_empty_db):

    url = '/recipe_create'
    header = {
        'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzODMwOTMzfQ"
                        ".z2O6YMEHnXD6l0vhfNNBoZS22_r33HGjtXCYBJ-5chE"}

    response = client_empty_db.post(url, headers=header)
    assert response.status_code == 401
    assert response.get_json() == {'message': 'Token is invalid.'}

