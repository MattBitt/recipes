from base_test import BaseTest
from pyquery import PyQuery as pq
from datetime import datetime, timedelta, date
from app.forms import RecipeForm
from app.models import Recipe
from app import app, db
from flask import render_template, flash, redirect, session, url_for, request, g
from app.views import search_recipes


def create_recipe():
     return Recipe(recipe_name = "Test Recipe", 
                ingredients = "2 eggs\nbacon",
                directions = "cook eggs \n in bacon grease",
                notes = "breakfast",
                url = "www.google.com",
                rating = 4,
                timestamp = date.today(),
                was_cooked = 1,
                user_id = 1)

def save_recipe( recipe ):
        db.session.add( recipe )
        db.session.commit()
        
   
    

class DB_Tests(BaseTest):   
    def test_add_recipe(self):
        r = create_recipe()
        db.session.add(r)
        db.session.commit()
        recs = Recipe.query.all()
        assert recs[0].id == 1

    def test_edit_recipe(self):
        r = Recipe.query.filter('id=1').first()
        r.ingredients = "4 eggs\nbacon\hasbrowns"
        db.session.add(r)
        db.session.commit()
        recipes = Recipe.query.all()
        assert recipes[0].id == 1
        assert recipes[0].ingredients == "4 eggs\nbacon\hasbrowns"
        assert recipes[0].recipe_name == "Test Recipe"
 
    def test_invalid_date(self):
        rec = Recipe.query.filter('id=1').first()
        self.ctx.push()
        rv = self.app.get(url_for('view_recipe', id=1))
        self.ctx.pop()
        assert rec.recipe_name in rv.data
        rec.timestamp = None
        save_recipe(rec)
        self.ctx.push()
        rv = self.app.get(url_for('view_recipe', id=1))
        assert rec.recipe_name in rv.data
        self.ctx.pop()

    def test_search(self):
        rec = search_recipes("blah")
        assert rec == []
        rec = search_recipes("Test")
        assert len(rec) == 1
        rec = search_recipes("bacon")
        assert len(rec) == 1
        
        


if __name__ == '__main__':
    unittest.main()