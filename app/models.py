from app import db
from app import app

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    recipe_name = db.Column(db.String(150))
    timestamp = db.Column(db.Date)
    user_id = db.Column(db.Integer)
    directions = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    notes = db.Column(db.Text)
    url = db.Column(db.String(150))
    image_path = db.Column(db.String(150))
    was_cooked = db.Column(db.Boolean)
    rating = db.Column(db.Integer)
            
    def __repr__(self):
        return '<Recipe %r - %r>' % (self.id, self.recipe_name)

   
