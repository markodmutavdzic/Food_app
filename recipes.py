import datetime
from functools import wraps

import jwt

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

from sqlalchemy import desc, asc
from sqlalchemy.sql.functions import count


from hunter import email_verifier
from marsh import user_register_schema, recipe_create_schema, recipe_rate_schema

app = Flask(__name__)
app.config['SECRET_KEY'] = 'marko'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0147@localhost:5432/Food_recipes'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0147@postgresdb/Food_recipes'

db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    user_location = db.Column(db.Text)
    user_title = db.Column(db.String(50))
    company_name = db.Column(db.String(50))
    company_sector = db.Column(db.String(50))
    recipes = db.relationship('Recipe', backref='user')


recipe_ingredient = db.Table('recipe_ingredient',
                             db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id')),
                             db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'))
                             )


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    text = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    rating = db.Column(db.Float)
    rating_sum = db.Column(db.Float)
    rating_count = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ingredient = db.relationship('Ingredient', secondary=recipe_ingredient,
                                 backref=db.backref('recipe', lazy='dynamic'))


class Ingredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])

            current_user = User.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message': 'Token is invalid.'}), 401

        current_user_id = current_user.id
        return f(current_user_id, *args, **kwargs)

    return decorated


@app.route('/user_registration', methods=['POST'])
def user_registration():
    try:
        data = user_register_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    user = User.query.filter_by(username=data['username']).first()
    if user:
        return jsonify({"message": "User with that username already exists."}), 400

    if not email_verifier(data['email']):
        return jsonify({"message": "Invalid email"}), 400

    new_user = User(first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=data['email'],
                    username=data['username'],
                    password=data['password'],
                    user_location="Clear",
                    user_title=None,
                    company_name=None,
                    company_sector=None,
                    )
    db.session.add(new_user)
    db.session.commit()
    db.session.close()

    return jsonify({"message": "New user created."}), 200


@app.route('/')
def nesto():
    db.create_all()
    return "123"



@app.route('/user_login')
def user_login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "Username and password required."}), 401

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return jsonify({"message": "User with that username doesn't exist"}), 401

    if user.password == auth.password:
        token = jwt.encode(
            {'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token}), 200

    return jsonify({"message": "Invalid password"}), 401


@app.route('/recipe_create', methods=['POST'])
@token_required
def recipe_create(current_user_id):

    try:
        data = recipe_create_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    name = data['name']
    text = data['text']
    ingredients = data['ingredients'].replace(',', ' ').split()

    existing_recipe = Recipe.query.filter_by(name=name).first()
    if existing_recipe:
        return jsonify({"message": "Recipe with that name already exists"}), 400

    new_recipe = Recipe(
        name=name,
        text=text,
        ingredients=str(ingredients),
        rating=0.0,
        rating_sum=0,
        rating_count=0,
        user_id=current_user_id
    )

    db.session.add(new_recipe)
    db.session.commit()
    db.session.close()

    ingredients_db = Ingredient.query.with_entities(Ingredient.name).all()
    ingredients_db_list = [r for (r,) in ingredients_db]

    for ingredient in list(ingredients):
        if ingredient not in ingredients_db_list:
            new_ingredient = Ingredient(name=ingredient)
            db.session.add(new_ingredient)
            db.session.commit()
            db.session.close()

    ingredient_object = Ingredient.query.all()
    for i in ingredient_object:
        if i.name in ingredients:
            i.recipe.append(new_recipe)

    db.session.commit()
    db.session.close()

    return jsonify({"message": "New recipe created."}), 200


@app.route('/recipe_rate', methods=['POST'])
@token_required
def recipe_rate(current_user_id):

    try:
        data = recipe_rate_schema.load(request.get_json())
    except ValidationError as err:
        return err.messages, 400

    recipe_id = data['recipe_id']
    rate = data['rate']

    recipe = Recipe.query.filter_by(id=recipe_id).first()
    if not recipe:
        return jsonify({"message": "Recipe with that id doesn't exist."}), 400
    if recipe.user_id == current_user_id:
        return jsonify({"message": "It's not allowed to rate your own recipes"}), 400

    recipe.rating_count = int(recipe.rating_count) + 1
    recipe.rating_sum = float(recipe.rating_sum) + float(rate)
    recipe.rating = round(recipe.rating_sum/recipe.rating_count, 2)

    db.session.commit()
    db.session.close()

    return jsonify({"message": "Recipe successfully rated"}), 200


def recipe_response(recipes_db):
    recipes = []
    for recipe in recipes_db:
        recipe_add = {
            "recipe id": recipe.id,
            "recipe name": recipe.name,
            "recipe text": recipe.text,
            "recipe ingredients": recipe.ingredients,
            "recipe rating": recipe.rating,
            "recipe user id": recipe.user_id,
        }
        recipes.append(recipe_add)
    return recipes


@app.route('/recipe_list_all')
def recipe_list_all():
    request_query = request.args.get('filter')
    request_page = request.args.get('page')
    if request_page:
        page = int(request_page)
    else:
        page = 1
    if not request_query:
        recipes_db = Recipe.query.order_by(Recipe.id).paginate(per_page=2, page=page, error_out=False)
    else:
        recipes_db = (
            db.session.query(Recipe).select_from(Ingredient).join(Ingredient.recipe)
            .group_by(Recipe.id)
            .order_by(desc(count(Ingredient.id)) if request_query == 'max' else asc(count(Ingredient.id)))
            .paginate(per_page=2, page=page, error_out=False)
        )

    if recipes_db.page > recipes_db.pages:
        return jsonify({"message": "You requested page that don't exist"},
                       {"current page": recipes_db.page},
                       {"total pages": recipes_db.pages}), 400

    recipes = recipe_response(recipes_db.items)
    return jsonify({"current page": recipes_db.page},
                   {"total pages": recipes_db.pages},
                   {"recipes": recipes}), 200


@app.route('/recipe_list_own')
@token_required
def recipe_list_own(current_user_id):

    recipes_db = Recipe.query.filter_by(user_id=current_user_id).all()
    recipes = recipe_response(recipes_db)
    return jsonify({"recipes": recipes}), 200


@app.route('/ingredients_top')
def ingredients_top():
    ingredient_top_db = (db.session.query(Ingredient).select_from(Recipe).join(Ingredient.recipe).group_by
                         (Ingredient.id).order_by(count(Recipe.id).desc()).limit(5))

    top_ingredients = [{i.name: i.recipe.count()} for i in ingredient_top_db]

    return jsonify({"Top 5 ingredients": top_ingredients}), 200


@app.route("/recipe_search")
def recipe_search():
    request_query_name = request.args.get('name')
    request_query_text = request.args.get('text')
    request_query_ingredients = request.args.get('ingredients')

    if request_query_name:
        recipes_list = Recipe.query.filter(Recipe.name.ilike(f'%{request_query_name}%')).all()
    elif request_query_text:
        recipes_list = Recipe.query.filter(Recipe.text.ilike(f'%{request_query_text}%')).all()
    elif request_query_ingredients:
        recipes_list = Recipe.query.filter(Recipe.text.ilike(f'%{request_query_ingredients}%')).all()

    else:
        return jsonify({"message": "Enter search parameter and value"}), 400

    if not recipes_list:
        return jsonify({"message" : "Recipe with that search parameter doesn't exist "})
    recipes = recipe_response(recipes_list)
    return jsonify({"message": recipes}), 200


if __name__ == '__main__':
    db.create_all()
    app.run(port=5000, host="0.0.0.0")
