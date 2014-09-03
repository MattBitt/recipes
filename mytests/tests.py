#!flask/bin/python
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../'))

import unittest
from datetime import datetime, timedelta, date
from app.models import Recipe
from config import basedir
from app import app, db
from app.scraper import scrape_recipe
from flask import url_for, session
from app.forms import RecipeForm
from pyquery import PyQuery as pq



def create_recipe():
     return Recipe(recipe_name = "Test Recipe", 
                ingredients = "2 eggs\nbacon",
                directions = "cook eggs \n in bacon grease",
                notes = "breakfast",
                url = "www.google.com",
                rating = 4,
                timestamp = date.today(),
                was_cooked = 1)

def save_recipe( recipe ):
        db.session.add( recipe )
        db.session.commit()
        
   
    

class TestCase(BaseTest):   
  

    def test_edit_recipe(self):
        r = create_recipe()
        db.session.add(r)
        db.session.commit()
        r.ingredients = "4 eggs\nbacon\hasbrowns"
        db.session.add(r)
        db.session.commit()
        recipes = Recipe.query.all()
        assert recipes[0].id == 1
        assert recipes[0].ingredients == "4 eggs\nbacon\hasbrowns"
        assert recipes[0].recipe_name == "Test Recipe"
 
    def test_invalid_date(self):
        r = create_recipe()
        save_recipe(r)
        rec = Recipe.query.filter('id=1').first()
        self.ctx.push()
        rv = self.app.get(url_for('view_recipe', id=1))
        self.ctx.pop()
        assert r.recipe_name in rv.data
        r.timestamp = None
        save_recipe(r)
        self.ctx.push()
        rv = self.app.get(url_for('view_recipe', id=1))
        self.ctx.pop()
        assert r.recipe_name in rv.data
    


if __name__ == '__main__':
    unittest.main()

    