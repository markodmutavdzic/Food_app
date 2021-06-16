def test_recipe_list_all(client_recipe_list_all):
    url = '/recipe_list_all'

    response = client_recipe_list_all.get(url)

    assert response.status_code == 200
    assert response.get_json() == {'recipes': [{'recipe id': 1,
                                                'recipe ingredients': 'water, flour',
                                                'recipe name': 'Bread',
                                                'recipe rating': 0.0,
                                                'recipe text': 'Mix water, flour and egg',
                                                'recipe user id': None},
                                               {'recipe id': 2,
                                                'recipe ingredients': 'water, flour, egg',
                                                'recipe name': 'Bread1',
                                                'recipe rating': 0.0,
                                                'recipe text': 'Mix water, flour and egg',
                                                'recipe user id': 1},
                                               {'recipe id': 3,
                                                'recipe ingredients': 'water',
                                                'recipe name': 'Bread2',
                                                'recipe rating': 0.0,
                                                'recipe text': 'Mix water, flour and egg',
                                                'recipe user id': None}]}


# def test_recipe_list_all_max(client_recipe_list_all):
#     url = 'recipe_list_all?filter=max'
#
#     response = client_recipe_list_all.get(url)
#
#     assert response.status_code == 200
#     assert response.get_json() == "123"
#
#
# def test_recipe_list_all_min(client_recipe_list_all):
#     url = 'recipe_list_all?filter=min'
#
#     response = client_recipe_list_all.get(url)
#
#     assert response.status_code == 200
#     assert response.get_json() == "123"