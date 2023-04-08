from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import json
import pandas as pd
import sqlite3
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static')
app.secret_key = "Messi"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/test1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


def importdb(dbb='init_db_food.db'):

    with app.app_context():
        dat = sqlite3.connect("init_db_food.db")
        query = dat.execute("SELECT * From main.food")
        cols = [col[0] for col in query.description]
        results = pd.DataFrame.from_records(data= query.fetchall(), columns=cols)
        profile = {}
        for index, row in results.iterrows():
            profile[index] = row
        for _, row in results.iterrows():
            food = Food(foodID=row['foodID'], foodName=row['foodName'], image=row['image'],
                        recipe=row['recipie'], ingredients=row['ingredients'], cost=row['cost'],
                        trackcountryID=row['trackcountryID'])
            try:
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


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'success')
    return redirect('/home')



@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_text = request.form.get('search')
        if search_text and search_text.strip():
            search_results = Food.query.filter(Food.foodName.like(f'%{search_text}%')).all()

            return render_template('search.html', search_results=search_results, search_text=search_text)
        else:
            return render_template('search.html', search_results=None, search_text=None)

    else:
        return render_template('search.html', search_results=None, search_text=None)

# make some alternatives if seacrh results
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
