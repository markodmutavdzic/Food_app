
import pytest

from recipes import app, db


@pytest.fixture
def patch_clearbit(mocker):
    return mocker.patch(
        "recipes.additional_data",
        return_value={'user_location': None, 'user_title': None, 'company_name': None, 'company_sector': None}
    )

@pytest.fixture
def client_empty_db():
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0147@localhost:5432/Food_recipes_test'

    with app.test_client() as client:
        db.create_all()
        db.session.commit()
        db.session.close()
        yield client
        db.session.remove()
        db.drop_all()

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