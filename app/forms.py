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
    directions = TextAreaField('Directions', validators = [DataRequired( message='Directions are required')])
    ingredients = TextAreaField('Ingredients', validators = [DataRequired( message='Ingredients are required')])
    notes = TextAreaField('Notes')
    url = TextField('URL', 
        validators = [URL(require_tld=False, message="Invalid URL"), Optional()])
    image_path = TextField('image_path')
    was_cooked = BooleanField('Cooked?')
    rating = IntegerField('Rating', validators = [NumberRange(min=1, max=5, message="Rating must be between 1 and 5"), Optional()])
    user_id = IntegerField('user_id')
    timestamp = DateField('Date', format='%Y-%m-%d')
    image_file = FileField('Image File')
    
    #test_url = URLField(validators=[url_validator()])
class SearchForm(Form):
    search = TextField('search', validators = [DataRequired()])
# class MyTextInput(TextInput):
    # def __init__(self, error_class=u'has_errors'):
        # super(MyTextInput, self).__init__()
        # self.error_class = error_class

    # def __call__(self, field, **kwargs):
        # if field.errors:
            # c = kwargs.pop('class', '') or kwargs.pop('class_', '')
            # kwargs['class'] = u'%s %s' % (self.error_class, c)
        # return super(MyTextInput, self).__call__(field, **kwargs)    

