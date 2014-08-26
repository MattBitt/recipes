#!flask/bin/python
import os
import unittest
from datetime import datetime, timedelta
from app.models import User, Recipe, Tag
from config import basedir
from app import app, db



class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
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
        r = Recipe(recipe_name = "Test Recipe", 
                ingredients = "2 eggs\nbacon",
                directions = "cook eggs \n in bacon grease",
                notes = "breakfast",
                url = "www.google.com",
                rating = 4,
                was_cooked = 1)
        db.session.add(r)
        db.session.commit()
        recipes = Recipe.query.all()
        assert recipes[0].id == 1
        assert recipes[0].ingredients == "2 eggs\nbacon"
        assert recipes[0].recipe_name == "Test Recipe"
 
 
 
    def test_edit_recipe(self):
        r = Recipe(recipe_name = "Test Recipe", 
                ingredients = "2 eggs\nbacon",
                directions = "cook eggs \n in bacon grease",
                notes = "breakfast",
                url = "www.google.com",
                rating = 4,
                was_cooked = 1)
        db.session.add(r)
        db.session.commit()
        r.ingredients = "4 eggs\nbacon\hasbrowns"
        db.session.add(r)
        db.session.commit()
        recipes = Recipe.query.all()
        assert recipes[0].id == 1
        assert recipes[0].ingredients == "4 eggs\nbacon\hasbrowns"
        assert recipes[0].recipe_name == "Test Recipe"
        
        
    def test_create_tags(self):
        new_tag = Tag(tag_name = "breakfast")
        db.session.add(new_tag)
        db.session.commit()
        tags = Tag.query.all()
        assert tags[0].tag_name == "breakfast"
        
    def test_delete_tag(self):
        new_tag = Tag(tag_name = "breakfast")
        db.session.add(new_tag)
        db.session.commit()
        tags = Tag.query.all()
        assert len(tags) == 1
        db.session.delete(tags[0])
        db.session.commit()
        tags = Tag.query.all()
        assert len(tags) == 0
        
    def test_add_tag(self):
        new_tag1 = Tag(tag_name = "breakfast")
        db.session.add(new_tag1)
        db.session.commit()
        new_recipe = Recipe(recipe_name = "Test Recipe", 
            ingredients = "2 eggs\nbacon",
            directions = "cook eggs \n in bacon grease",
            notes = "breakfast",
            url = "www.google.com",
            rating = 4,
            was_cooked = 1)
        db.session.add(new_recipe)
        db.session.commit()
        assert new_recipe.has_tag( new_tag1 ) == False
        new_recipe.add_tag(new_tag1)
        assert new_recipe.has_tag( new_tag1 ) == True
        assert len(new_recipe.my_tags) == 1
        new_recipe.add_tag(new_tag1)
        assert len(new_recipe.my_tags) == 1
        new_tag2 = Tag(tag_name = "lunch")
        new_recipe.add_tag(new_tag2)
        assert len(new_recipe.my_tags) == 2
        new_recipe.remove_tag(new_tag2)
        assert len(new_recipe.my_tags) == 1
    
    
    
    def test_find_recipes_with_tag(self):
        new_tag = Tag(tag_name = "breakfast")
        db.session.add(new_tag)
        db.session.commit()
        new_recipe = Recipe(recipe_name = "Test Recipe #2")
        new_recipe.add_tag(new_tag)
        db.session.add(new_recipe)
        db.session.commit()
        assert len(new_tag.recipe.all()) == 1
        new_recipe = Recipe(recipe_name = "Test Recipe")
        new_recipe.add_tag(new_tag)
        db.session.add(new_recipe)
        db.session.commit()

        assert len(new_tag.recipe.all()) == 2
        
        new_tag2 = Tag(tag_name = "lunch")
        new_recipe.add_tag(new_tag2)
        db.session.add(new_recipe)
        db.session.commit()
        
        assert len(new_tag2.recipe.all()) == 1
        

#        t = Tag.query.filter_by(id =1).first()
        #import pdb; pdb.set_trace()
#        rec =  Recipe.query.all()
#        print rec[0].my_tags
        
        
        
if __name__ == '__main__':
    unittest.main()