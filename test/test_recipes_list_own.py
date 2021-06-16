from freezegun import freeze_time


@freeze_time('2021-06-16 07:43:06.284695')
def test_recipes_list_own(client_recipe_list_all):
    url = '/recipe_list_own'
    header = {
        'access-token': "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzODMwOTMzfQ"
                        ".z2O6YMEHnXD6l0vhfNNBoZS22_r33HGjtXCYBJ-5chE"}
    response = client_recipe_list_all.get(url, headers=header)

    assert response.status_code == 200
    assert response.get_json() == {'recipes': [{'recipe id': 2,
                                                'recipe ingredients': 'water, flour, egg',
                                                'recipe name': 'Bread1',
                                                'recipe rating': 0.0,
                                                'recipe text': 'Mix water, flour and egg',
                                                'recipe user id': 1}]}
