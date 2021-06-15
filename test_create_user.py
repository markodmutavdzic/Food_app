import pytest

from recipes import app, db


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