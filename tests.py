#!flask/bin/python
import os
import unittest
from datetime import datetime, timedelta, date
from app.models import User, Recipe
from config import basedir
from app import app, db
from app.scraper import scrape_recipe
from flask import url_for, session



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
        
        
def create_user():
    u =  User(name = 'Matt', email='mizzle@gmail.com',password='pass')
    db.session.add(u)
    db.session.commit()
    return u


    
class BaseCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        db.create_all()
        self.ctx = app.test_request_context()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
class TestCasa(BaseCase):   
  
    def test_add_recipe(self):
        r = create_recipe()
        db.session.add(r)
        db.session.commit()
        recipes = Recipe.query.all()
        assert recipes[0].id == 1
        assert recipes[0].ingredients == "2 eggs\nbacon"
        assert recipes[0].recipe_name == "Test Recipe"
 
 
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
    
    def test_create_user(self):
        u  = create_user()
        newuser = User.query.filter('email="mizzle@gmail.com"').first()
        assert u.name == newuser.name
        assert u.email == newuser.email
        assert u.pwdhash == newuser.pwdhash
    
  
if __name__ == '__main__':
    unittest.main()