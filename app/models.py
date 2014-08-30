from app import db
from app import app
from werkzeug import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
import md5
from itsdangerous import URLSafeTimedSerializer

def hash_pass(password):
    """
    Return the md5 hash of the password+salt
    """
    salted_password = password + app.secret_key
    return md5.new(salted_password).hexdigest()

@login_manager.user_loader
def load_user(username):
    return get_user( username )
 
@login_manager.token_loader
def load_token(token):
    """
    Flask-Login token_loader callback. 
    The token_loader function asks this function to take the token that was 
    stored on the users computer process it to check if its valid and then 
    return a User Object if its valid or None if its not valid.
    """
 
    #The Token itself was generated by User.get_auth_token.  So it is up to 
    #us to known the format of the token data itself.  
 
    #The Token was encrypted using itsdangerous.URLSafeTimedSerializer which 
    #allows us to have a max_age on the token itself.  When the cookie is stored
    #on the users computer it also has a exipry date, but could be changed by
    #the user, so this feature allows us to enforce the exipry date of the token
    #server side and not rely on the users cookie to exipre. 
    max_age = app.config["REMEMBER_COOKIE_DURATION"].total_seconds()
 
    #Decrypt the Security Token, data = [username, hashpass]
    data = login_serializer.loads(token, max_age=max_age)
 
    #Find the User
    user = get_user( data[0] )
 
    #Check Password and return user or None
    if user and data[1] == user.password:
        return user
    return None    
    
def get_user( user_name ):    
    u = User.query.filter_by(user_name = user_name).first()
    return u
    
    
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(54))
    recipes = db.relationship('Recipe', backref = 'poster', lazy = 'dynamic')
    
    def __init__(self,user_name, password):
        self.user_name = user_name
        self.password = password
    
    def get_auth_token(self):
        """
        Encode a secure token for cookie
        """
                                   
        login_serializer = URLSafeTimedSerializer(app.secret_key)
        data = [str(self.user_name), self.password]
        return login_serializer.dumps(data)   
    
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

   
