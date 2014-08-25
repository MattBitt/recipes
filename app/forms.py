from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length
from app.models import User

class LoginForm(Form):
    openid = TextField('openid', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)
    
class RecipeForm(Form):
    recipe_name = TextField('recipe_name', validators = [DataRequired()])
    directions = TextAreaField('directions', validators = [Length(min = 0, max = 140)])
    ingredients = TextAreaField('ingredients', validators = [Length(min = 0, max = 140)])
    notes = TextAreaField('notes', validators = [Length(min = 0, max = 140)])
    url = TextField('recipe_url')
    image_path = TextField('recipe_name')
    was_cooked = BooleanField('was_cooked')
    rating = IntegerField('rating')
