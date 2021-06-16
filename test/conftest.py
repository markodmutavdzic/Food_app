import pytest

from recipes import User, app, db, Recipe

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

test_recipe = Recipe(
    name='Bread',
    text='Mix water, flour and egg',
    rating=0.0,
    ingredients='',
    user_id=None
)

test_recipe_own = Recipe(
    name='Bread',
    text='Mix water, flour and egg',
    rating=0.0,
    ingredients='',
    user_id=1
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
        db.make_transient(test_user)
        db.session.remove()
        db.drop_all()


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


@pytest.fixture
def patch_clearbit(mocker):
    return mocker.patch(
        "recipes.additional_data",
        return_value={'user_location': None, 'user_title': None, 'company_name': None, 'company_sector': None}
    )


@pytest.fixture()
def patch_jwt(mocker):
    return mocker.patch(
        "recipes.jwt.encode", return_value="123"
    )


@pytest.fixture
def client_recipe_rate():
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0147@localhost:5432/Food_recipes_test'

    with app.test_client() as client:
        db.create_all()
        db.session.add(test_user)
        db.session.commit()
        db.session.add(test_recipe)
        db.session.commit()
        db.session.close()
        yield client
        db.make_transient(test_user)
        db.make_transient(test_recipe)
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client_recipe_rate_own():
    app.config["TESTING"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0147@localhost:5432/Food_recipes_test'

    with app.test_client() as client:
        db.create_all()
        db.session.add(test_user)
        db.session.commit()
        db.session.add(test_recipe_own)
        db.session.commit()
        db.session.close()
        yield client
        db.make_transient(test_user)
        db.make_transient(test_recipe_own)
        db.session.remove()
        db.drop_all()