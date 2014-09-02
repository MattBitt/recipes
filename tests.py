#!flask/bin/python
import os
import unittest
from datetime import datetime, timedelta, date
from app.models import Recipe
from config import basedir
from app import app, db
from app.scraper import scrape_recipe
from flask import url_for, session
from wtforms_test import FormTestCase
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
        
def create_post_data():
    return {
        'ingredients'    :  'ham\n 2lbs bacon\n eggs',
        'directions'      :  'cook everything\n then eat',
        'recipe_name' : 'My   Recipe',
        'url'                   :  'http://www.google.com',
        'rating'             :  '5',
        'was_cooked' : '1',
        'image_path'   : 'app/static/pictures/mypic.jpg',
        'timestamp'     :  str(date.today())
    }
     
def check_invalid_input( bad_data, field, keyword, rv ):
        data = create_post_data()
        data[field] = bad_data
        q = pq(rv.data)
        alerttext = q('.help-inline').text()
        return keyword in alertext       
    
class BaseCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config.TestingConfig')
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        self.ctx = app.test_request_context()

    def tearDown(self):
        db.session.remove()

class TestCase(BaseCase):   
  
    #def test_add_recipe(self):
        # r = create_recipe()
        # db.session.add(r)
        # db.session.commit()
        # recipes = Recipe.query.all()
        # assert recipes[0].id == 1
        # assert recipes[0].ingredients == "2 eggs\nbacon"
        # assert recipes[0].recipe_name == "Test Recipe"

 
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
    
    def test_add_recipe(self):
        rv = self.app.get('/add_recipe/')
        
        # Make sure we got an OK response
        self.assertEqual(rv.status_code, 200)
        
        data = {}
        
        # Posting empty data to signup for should generate alerts
        rv = self.app.post('/add_recipe/', data=data)
        self.assertEqual(rv.status_code, 200)
        q = pq(rv.data)
        alerttext = q('.help-inline').text()
        assert 'Recipe Name' in alerttext
        assert 'Ingredients' in alerttext
        assert 'Directions' in alerttext
        
        # Now submitting with "real" data should not produce errors
        #    and should result in new database entries
        data = create_post_data()   
        
        rv = self.app.post('/add_recipe/', data=data)
        assert 'Invalid data' not in rv.data
        #assert 'changes have been saved' in rv.data
        self.assertEqual(rv.status_code, 302)       # On success we redirect
        
        r = Recipe.query.filter_by(recipe_name = data['recipe_name']).all()
        app.logger.info(r)
        self.assertEqual(len(r), 1, 'Incorrect number of recipes created')
        self.assertEqual(r[0].directions, data['directions'])
        self.assertEqual(r[0].timestamp, date.today())
        
        rv = self.app.post('/add_recipe/', data=data)
        assert check_invalid_input('www.google.com','url','URL', rv.data) == False


if __name__ == '__main__':
    unittest.main()

    