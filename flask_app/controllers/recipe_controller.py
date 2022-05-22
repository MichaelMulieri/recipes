
   
from crypt import methods
from flask import render_template, session,flash,redirect, request
import re
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipes/form')
def recipes_form():
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        "id":session['user_id']
    }
    return render_template('recipes_form.html', user=User.get_one(data))

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/form')

    data={
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made" : request.form['date_made'],
        "under_30" : int(request.form['under_30']),
        "user_id" : session['user_id']
    }
    Recipe.add_recipe(data)
    return redirect('/dashboard')

@app.route('/view/instructions/<int:id>')
def view_instructions(id):
    data = {
        "id":id
    }
    this_recipe = Recipe.show_one(data)
    user = User.get_one(data)
    return render_template('view_instructions.html', this_recipe = this_recipe, user = user)

@app.route('/destroy/<int:id>')
def destroy(id):
    data = {
        "id":id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')

@app.route('/edit/<int:id>')
def edit_page(id):
    data = {
        "id" : id
    }
    this_recipe = Recipe.show_one(data)
    user = User.get_one(data)
    print(this_recipe[0])
    return render_template('edit.html', this_recipe = this_recipe, user = user)

@app.route('/edit/recipe/<int:id>', methods = ['POST'])
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/edit/{id}')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
        "under_30": request.form['under_30'],
        "user_id": session['user_id'],
        "id": id
    }
    Recipe.edit(data)
    return redirect('/dashboard')
        
