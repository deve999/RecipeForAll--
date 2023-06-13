from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pandas as pd
import sqlite3
import random
from sqlalchemy.sql.expression import func
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static')
app.secret_key = "Messi"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/FoodForDays'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
COUNTRY_IDS = {
    "American": 1,
    "British": 2,
    "Chinese": 3,
    "Italian": 4
}

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)


class Food(db.Model):
    foodID = db.Column(db.Integer, primary_key=True)
    foodName = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200), nullable=False)
    recipe = db.Column(db.String(1000), nullable=False)
    ingredients = db.Column(db.String(500), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    trackcountryID = db.Column(db.Integer, nullable=False)


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.foodID'), nullable=False)
    user = db.relationship("User", backref=db.backref("favorites", cascade="all, delete-orphan"))
    food = db.relationship("Food", backref=db.backref("favorites", cascade="all, delete-orphan"))


def importdb(dbb='init_db_food3.db'):
    with app.app_context():
        dat = sqlite3.connect(dbb)
        query = dat.execute("SELECT * From main.food")
        cols = [col[0] for col in query.description]
        results = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
        profile = {}
        for index, row in results.iterrows():
            profile[index] = row
        for _, row in results.iterrows():
            food = Food(foodID=row['foodID'], foodName=row['foodName'], image=row['image'],
                        recipe=row['recipie'], ingredients=row['ingredients'], cost=row['cost'],
                        trackcountryID=row['trackcountryID'])
            try:
                existing_food = Food.query.filter_by(foodID=row['foodID']).first()
                if existing_food:
                    existing_food.foodName = row['foodName']
                    if not existing_food.image:  # Only update the image if it's not already set
                        existing_food.image = row['image']
                    existing_food.recipe = row['recipie']
                    existing_food.ingredients = row['ingredients']
                    existing_food.cost = row['cost']
                    existing_food.trackcountryID = row['trackcountryID']
                else:
                    db.session.add(food)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                continue



@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    foods = Food.query.all()
    return render_template('index.html', foods=foods)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('You have logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or '/home')
        else:
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_password = generate_password_hash(password, method='sha256')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('signup'))
        new_user = User(name=name, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('You have signed up successfully. Please log in to continue.', 'success')
        next_page = request.args.get('next')
        if next_page:
            return redirect('/login?next=' + next_page)
        else:
            return redirect('/login')
    else:
        return render_template('register.html')


@app.route('/country/<country>', methods=['GET'])
def country(country):
    trackcountryID = COUNTRY_IDS.get(country)
    if trackcountryID is None:
        flash(f"No recipes found for country: {country}", "warning")
        return redirect(url_for('homepage'))  # or wherever you want to redirect

    foods = Food.query.filter_by(trackcountryID=trackcountryID).all()
    if foods:
        return render_template('country.html', foods=foods, country=country)
    else:
        flash(f"No recipes found for country: {country}", "warning")
        return redirect(url_for('homepage'))  # or wherever you want to redirect


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return redirect('/home')


import random
from sqlalchemy.sql.expression import func

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_text = request.form.get('search')
        if search_text and search_text.strip():
            search_results = Food.query.filter(Food.foodName.like(f'%{search_text}%')).all()
            # if no results found, fetch a random country's food
            if not search_results:
                random_country = random.choice(list(COUNTRY_IDS.values()))
                print(search_results, "in not")
                search_results = Food.query.filter(Food.trackcountryID == random_country).order_by(func.random()).limit(10).all()
            return render_template('search.html', search_results=search_results, search_text=search_text)
        else:
            return render_template('search.html', search_results=None, search_text=None)

    else:
        return render_template('search.html', search_results=None, search_text=None)


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    user_id = session.get('user_id')
    if not user_id:
        flash('You need to log in to edit your preferences.', 'danger')
        return redirect(url_for('login'))
    user = User.query.get(user_id)
    if request.method == 'POST':
        new_name = request.form.get('name')
        new_username = request.form.get('username')
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        if new_name and new_name.strip():
            user.name = new_name.strip()
        if new_username and new_username.strip():
            existing_user = User.query.filter_by(username=new_username).first()
            if existing_user and existing_user.id != user.id:
                flash('Username already exists. Please choose a different username.', 'danger')
                return render_template('acc_settings.html', user=user)
            user.username = new_username.strip()
        if old_password and new_password and new_password.strip():
            if len(new_password.strip()) < 8 or not any(char.isdigit() for char in new_password):
                flash('New password must have at least 8 characters and include at least one number.', 'danger')
                return render_template('acc_settings.html', user=user)
            if not check_password_hash(user.password, old_password):
                flash('Old password is incorrect.', 'danger')
                return render_template('acc_settings.html', user=user)
            user.password = generate_password_hash(new_password, method='sha256')
        db.session.commit()
        flash('Your preferences have been updated.', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('acc_settings.html', user=user)


@app.route('/recipe/<int:food_id>')
def show_recipe(food_id):
    food = Food.query.get(food_id)
    if food:
        return render_template('recipe.html', food=food)
    else:
        flash('Food not found.', 'danger')
        return redirect(url_for('home'))


@app.route('/favorite/add', methods=['POST'])
def add_favorite():
    print("in add")
    food_id = request.form.get('food_id')
    # print(food_id)
    user_id = session.get('user_id')
    if user_id:
        fav = Favorite.query.filter_by(user_id=user_id, food_id=food_id).first()
        if not fav:
            new_favorite = Favorite(user_id=user_id, food_id=food_id)
            db.session.add(new_favorite)
            db.session.commit()
        else:
            remove_favorite(food_id)
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'not logged in'}), 401


@app.route('/favorite/remove/<int:food_id>', methods=['DELETE'])
def remove_favorite(food_id):
    print("in remove")
    user_id = session.get('user_id')
    if user_id:
        fav = Favorite.query.filter_by(user_id=user_id, food_id=food_id).first()
        # print(fav)
        if fav:
            # print(True)
            db.session.delete(fav)
            db.session.commit()
        else:
            add_favorite()
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'not logged in'}), 401


@app.route('/favorites', methods=['GET'])
def show_favorites():
    user_id = session.get('user_id')
    if user_id:
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        print("in favorites")
        return render_template('favorites.html', favorites=favorites)
    else:
        return redirect(url_for('login'))

# make some alternatives if search results
# work on react code and angular code


@app.context_processor
def inject_user():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return dict(user=user)
    else:
        return dict(user=None)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    importdb()
    app.run(debug=True)
