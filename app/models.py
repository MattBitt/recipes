from app import db
from app import app
from werkzeug import generate_password_hash, check_password_hash

ROLE_USER = 0
ROLE_ADMIN = 1

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    role = db.Column(db.SmallInteger, default = ROLE_USER)
    pwdhash = db.Column(db.String(54))
    recipes = db.relationship('Recipe', backref = 'poster', lazy = 'dynamic')
    
    def __init__(self, name, email, password):
        self.name = name.title()
        self.email = email.lower()
        self.set_password(password)
     
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)    
 

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    recipe_name = db.Column(db.String(150))
    timestamp = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    directions = db.Column(db.Text)
    ingredients = db.Column(db.Text)
    notes = db.Column(db.Text)
    url = db.Column(db.String(150))
    image_path = db.Column(db.String(150))
    was_cooked = db.Column(db.Boolean)
    rating = db.Column(db.Integer)
            
    def __repr__(self):
        return '<Recipe %r - %r>' % (self.id, self.recipe_name)

   
