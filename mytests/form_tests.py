from base_test import BaseTest
from pyquery import PyQuery as pq
from datetime import datetime, timedelta, date
from app.forms import RecipeForm
from app.models import Recipe
from app import app, db
from db_tests import create_recipe
from flask import url_for, g

def create_post_data():
    return {
        'ingredients'    :  'ham\n 2lbs bacon\n eggs',
        'directions'      :  'cook everything\n then eat',
        'recipe_name' : 'My  Recipe',
        'url'                   :  'http://www.google.com',
        'rating'             :  '5',
        'was_cooked' : '1',
        'image_path'   : 'app/static/pictures/mypic.jpg',
        'timestamp'     :  str(date.today())
    }
     
def check_invalid_input( bad_data, field, keyword, rv ):
        data = create_post_data()
        data[field] = bad_data
        q = pq(rv)
        alerttext = q('.help-inline').text()
        print alerttext
        return keyword in alerttext    



class FormTests(BaseTest):
    def test_add_recipe(self):
        app.logger.debug('Add recipe test')
        rv = self.app.get('/add_recipe/')
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
    
        data = create_post_data()   
        
        rv = self.app.post('/add_recipe/', data=data)
        assert 'Invalid data' not in rv.data
        self.assertEqual(rv.status_code, 302)       # On success we redirect
        
        r = Recipe.query.filter_by(recipe_name = data['recipe_name']).all()
        #app.logger.info(r)
        self.assertEqual(len(r), 1, 'Incorrect number of recipes created')
        self.assertEqual(r[0].directions, data['directions'])
        self.assertEqual(r[0].timestamp, date.today())
    

    def test_invalid_urls(self):
        app.logger.debug('Invalid URL Test')
        # Currently will validate following URL's
        # 'ttp://asdf.com']#
        
        bad_urls = ['www.google', 'matt']
        
        for b in bad_urls:
            data = create_post_data()
            data['url'] = b
            rv = self.app.post('/add_recipe/', data=data)
            q = pq(rv.data)
            alerttext = q('.help-inline').text()
            assert 'URL' in alerttext