from crypt import methods
from flask_app import app
from flask import render_template, request, redirect, flash, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def save_user():
    if not User.validate_user(request.form):
        return redirect('/')
    data={
        "first_name" :request.form['first_name'],
        "last_name" : request.form['last_name'],
        "email" : request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'id': session['user_id']
    }
    user = User.get_one(data)
    recipes = Recipe.all_recipes(data)
    print(recipes)
    print(user)
    return render_template('dashboard.html', user = user, recipes = recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

