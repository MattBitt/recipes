from base_test import BaseTest

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
        q = pq(rv)
        alerttext = q('.help-inline').text()
        return keyword in alerttext    



class FormTest(BaseTest):
    def test_add_recipe(self):
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
        app.logger.info(r)
        self.assertEqual(len(r), 1, 'Incorrect number of recipes created')
        self.assertEqual(r[0].directions, data['directions'])
        self.assertEqual(r[0].timestamp, date.today())
        
        rv = self.app.post('/add_recipe/', data=data)
        bad_urls = ['www.google.com', 'ttp://asdf.com', 'http://www.yahoo.com']
        for b in bad_urls:
            assert check_invalid_input(b,'url','URL', rv.data) == False