from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re

db = 'recipe'
class Recipe:
    def __init__(self, data):
        self.id=data['id']
        self.name = data['name']
        self.under_30 = data['under_30']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def all_recipes(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL(db).query_db(query, data)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        return recipes

    @classmethod
    def add_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id) VALUES \
            (%(name)s,%(description)s,%(instructions)s,%(date_made)s,%(under_30)s,%(user_id)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def show_one(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM recipes WHERE recipes.id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def edit(cls,data):
        query ="UPDATE recipes SET name=%(name)s, description=%(description)s, \
            instructions=%(instructions)s, date_made=%(date_made)s, under_30=%(under_30)s WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        if len(data['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters")
        if len(data['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters")
        if len(data['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters")
        if data['date_made'] == "":
            is_valid = False
            flash("You must include a date made")
        if 'under_30' not in data:
            is_valid = False
            flash("You must include cooking time")
        return is_valid

