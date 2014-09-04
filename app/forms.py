from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, IntegerField, widgets, DateField, FileField
from wtforms import SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, URL, Optional, NumberRange, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from app.models import Recipe
from app import db
from wtforms.fields.html5 import URLField
from wtforms.validators import url as url_validator
from flask.ext.uploads import UploadSet, IMAGES


images = UploadSet('images', IMAGES)

class RecipeForm(Form):
    recipe_name = TextField('Recipe Name' , validators = [DataRequired( message='Recipe Name is required')])
    directions = TextAreaField('Directions', validators = [Length(min = 0, max = 3000), DataRequired( message='Directions are required')])
    ingredients = TextAreaField('Ingredients', validators = [Length(min = 0, max = 3000), DataRequired( message='Ingredients are required')])
    notes = TextAreaField('Notes', validators = [Length(min = 0, max = 3000)])
    url = TextField('URL', 
        validators = [URL(require_tld=False, message="Invalid URL"), Optional()])
    image_path = TextField('image_path')
    was_cooked = BooleanField('Cooked?')
    rating = IntegerField('Rating', validators = [NumberRange(min=1, max=5, message="Rating must be between 1 and 5"), Optional()])
    user_id = IntegerField('user_id')
    timestamp = DateField('Date', format='%Y-%m-%d')
    image_file = FileField('Image File')
    #test_url = URLField(validators=[url_validator()])
    

