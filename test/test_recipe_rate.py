from freezegun import freeze_time




@freeze_time('2021-06-16 07:43:06.284695')
def test_recipe_rate(client_recipe_rate):
    data = {
            "recipe_id": 1,
            "rate": 5
}
    url = '/recipe_rate'
    header = {
        'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzODMwOTMzfQ"
                        ".z2O6YMEHnXD6l0vhfNNBoZS22_r33HGjtXCYBJ-5chE"}
    response = client_recipe_rate.post(url, headers=header, json=data)

    assert response.status_code == 200
    assert response.get_json() == {'message': 'Recipe successfully rated'}


@freeze_time('2021-06-16 07:43:06.284695')
def test_recipe_rate_missing_id(client_recipe_rate):
    data = {

            "rate": 5
}
    url = '/recipe_rate'
    header = {
        'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzODMwOTMzfQ"
                        ".z2O6YMEHnXD6l0vhfNNBoZS22_r33HGjtXCYBJ-5chE"}
    response = client_recipe_rate.post(url, headers=header, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'recipe_id': ['Missing data for required field.']}


@freeze_time('2021-06-16 07:43:06.284695')
def test_recipe_rate_missing_rate(client_recipe_rate):
    data = {
            "recipe_id": 1,

}
    url = '/recipe_rate'
    header = {
        'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzODMwOTMzfQ"
                        ".z2O6YMEHnXD6l0vhfNNBoZS22_r33HGjtXCYBJ-5chE"}
    response = client_recipe_rate.post(url, headers=header, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'rate': ['Missing data for required field.']}


@freeze_time('2021-06-16 07:43:06.284695')
def test_recipe_rate_unknown_recipe(client_recipe_rate):
    data = {
            "recipe_id": 3,
            "rate": 5
}
    url = '/recipe_rate'
    header = {
        'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzODMwOTMzfQ"
                        ".z2O6YMEHnXD6l0vhfNNBoZS22_r33HGjtXCYBJ-5chE"}
    response = client_recipe_rate.post(url, headers=header, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'message': "Recipe with that id doesn't exist."}


@freeze_time('2021-06-16 07:43:06.284695')
def test_recipe_rate_own(client_recipe_rate_own):
    data = {
            "recipe_id": 1,
            "rate": 5
}
    url = '/recipe_rate'
    header = {
        'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzODMwOTMzfQ"
                        ".z2O6YMEHnXD6l0vhfNNBoZS22_r33HGjtXCYBJ-5chE"}
    response = client_recipe_rate_own.post(url, headers=header, json=data)

    assert response.status_code == 400
    assert response.get_json() == {'message': "It's not allowed to rate your own recipes"}