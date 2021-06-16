import pytest

from recipes import User, app, db

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
        db.session.commit()
        db.make_transient(test_user)
        db.session.remove()
        db.drop_all()

def test_user_login(client_one_user_db, patch_jwt):
    url = '/user_login'
    response = client_one_user_db.get(url, auth=("mare", "0147"))

    assert response.status_code == 200
    assert response.get_json() == {"token": "123"}

def test_user_login_no_auth(client_empty_db):
    url = '/user_login'
    response = client_empty_db.get(url)

    assert response.status_code == 401
    assert response.get_json() == {'message': 'Username and password required.'}


def test_user_login_wrong_username(client_empty_db):
    url = '/user_login'
    response = client_empty_db.get(url, auth=("test_user", "test_password"))

    assert response.status_code == 401
    assert response.get_json() == {'message': "User with that username doesn't exist"}


def test_user_login_wrong_password(client_one_user_db):
    url = '/user_login'
    response = client_one_user_db.get(url, auth=('mare', "test_pass"))

    assert response.status_code == 401
    assert response.get_json() == {'message': 'Invalid password'}




