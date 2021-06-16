

def test_recipe_search_no_params(client_recipe_list_all):
    url = '/recipe_search'
    response = client_recipe_list_all.get(url)
    assert response.status_code == 400
    assert response.get_json() == {'message': 'Enter search parameter and value'}


# def test_recipe_search_name(client_recipe_list_all):
#     url = '/recipe_search?name=Bread'
#     response = client_recipe_list_all.get(url)
#     assert response.status_code == 400
#     assert response.get_json() == "123"
#
#
# def test_recipe_search_text(client_recipe_list_all):
#     url = '/recipe_search?text=water'
#     response = client_recipe_list_all.get(url)
#     assert response.status_code == 400
#     assert response.get_json() == "123"
#
#
# def test_recipe_search_ingredients(client_recipe_list_all):
#     url = '/recipe_search?ingredients=water'
#     response = client_recipe_list_all.get(url)
#     assert response.status_code == 400
#     assert response.get_json() == "123"