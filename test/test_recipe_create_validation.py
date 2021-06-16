import pytest
from freezegun import freeze_time

from recipes import app, db, User

test_user = User(first_name='Marko',
                 last_name='Mutavdzic',
                 email='marko.mutavdzic@factoryww.com',
                 username='mare',
                 password='0147',
                 user_location=None,
                 user_title=None,
                 company_name=None,
                 company_sector=None
                 )


@pytest.fixture
def client_one_user_db():
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0147@localhost:5432/Food_recipes_test'

    with app.test_client() as client:
        db.create_all()
        db.session.add(test_user)
        db.session.commit()
        db.session.close()
        yield client
        db.session.delete(test_user)
        db.session.remove()


@freeze_time('14-06-2021 12:41:00')
def test_recipe_create_missing_name(client_one_user_db):
    data = {
        "name": "Bread",
        "text": "Mix water, flour and egg",
        "ingredients": "water, flour, egg"
    }
    url = '/recipe_create'
    header = {
        'access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZXhwIjoxNjIzNjY4OTQzfQ.'
                        'PvjsLpF1xKOVP7DEYrG7Ubv-XdWjz7WnJPdHZ6ZjT4s'}
    response = client_one_user_db.post(url,headers=header, json=data)

    assert response.data == "123"
