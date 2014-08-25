from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, URL, Optional, NumberRange
from app.models import User

def format_url(data):
        if data[:4].upper() != "HTTP":
            return "http://" + data
        return data


class LoginForm(Form):
    openid = TextField('openid', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)
    
class RecipeForm(Form):
    recipe_name = TextField('recipe_name', validators = [DataRequired()])
    directions = TextAreaField('directions', validators = [Length(min = 0, max = 140)])
    ingredients = TextAreaField('ingredients', validators = [Length(min = 0, max = 140)])
    notes = TextAreaField('notes', validators = [Length(min = 0, max = 140)])
    url = TextField('recipe_url', 
        validators = [URL(require_tld=False, message="Invalid URL"), Optional()],
        filters = [format_url]) 
        
    image_path = TextField('recipe_name')
    was_cooked = BooleanField('was_cooked')
    rating = IntegerField('rating', validators = [NumberRange(min=1, max=5, message="Rating must be between 1 and 5"), Optional()])

