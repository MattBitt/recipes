from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, IntegerField, widgets, DateField, FileField
from wtforms import SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, URL, Optional, NumberRange, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from app.models import Recipe
from app import db


class RecipeForm(Form):
    recipe_name = TextField('recipe_name' , validators = [DataRequired( message='Recipe Name is required')])
    directions = TextAreaField('directions', validators = [Length(min = 0, max = 3000), DataRequired( message='Directions are required')])
    ingredients = TextAreaField('ingredients', validators = [Length(min = 0, max = 3000), DataRequired( message='Ingredients are required')])
    notes = TextAreaField('notes', validators = [Length(min = 0, max = 3000)])
    url = TextField('recipe_url', 
        validators = [URL(require_tld=False, message="Invalid URL"), Optional()])
    image_path = TextField('image_path')
    was_cooked = BooleanField('was_cooked')
    rating = IntegerField('rating', validators = [NumberRange(min=1, max=5, message="Rating must be between 1 and 5"), Optional()])
    user_id = IntegerField('user_id')
    timestamp = DateField('timestamp', format='%Y-%m-%d')
    image_file = FileField('image_file')
    
