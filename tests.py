#!flask/bin/python
import os
import unittest
from datetime import datetime, timedelta
from app.models import User, Recipe
from config import basedir
from app import app, db
from app.scraper import scrape_recipe
from flask import url_for

def create_recipe():
     return Recipe(recipe_name = "Test Recipe", 
                ingredients = "2 eggs\nbacon",
                directions = "cook eggs \n in bacon grease",
                notes = "breakfast",
                url = "www.google.com",
                rating = 4,
                was_cooked = 1)
                

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_make_unique_nickname(self):
        u = User(nickname = 'john', email = 'john@example.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('john')
        assert nickname != 'john'
        u = User(nickname = nickname, email = 'susan@example.com')
        db.session.add(u)
        db.session.commit()
        nickname2 = User.make_unique_nickname('john')
        assert nickname2 != 'john'
        assert nickname2 != nickname
    
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
    
    def test_scrape_all_recipes(self):
        url = "http://allrecipes.com/Recipe/Grilled-Salmon-I/Detail.aspx?soid=carousel_0_rotd&prop24=rotd"
        rec = scrape_recipe( url )
        assert rec.get_title() == "Grilled Salmon I"
        assert "lemon pepper to taste" in rec.get_ingredients()
        assert "vegetable oil until" in rec.get_directions()
  
    def test_scrape_skinny_taste(self):
        url = 'http://www.skinnytaste.com/2014/08/asian-farro-medley-with-salmon.html'
        rec = scrape_recipe( url )
        assert rec.get_title() == "Asian Farro Medley with Salmon"
        assert "1 tbsp oyster sauce" in rec.get_ingredients()
        assert "salmon to marinade and set" in rec.get_directions()
    
        
if __name__ == '__main__':
    unittest.main()