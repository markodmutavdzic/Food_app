

def test_ingredients_top(client_recipe_list_all):
    url = '/ingredients_top'
    response = client_recipe_list_all.get(url)

    assert response.status_code == 200
    assert response.get_json() == {'Top 5 ingredients': []}