from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, IntegerField, widgets
from wtforms.validators import DataRequired, Length, URL, Optional, NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from app.models import User, Tag, Recipe




class LoginForm(Form):
    openid = TextField('openid', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)
    
class RecipeForm(Form):
    recipe_name = TextField('recipe_name', validators = [DataRequired()])
    directions = TextAreaField('directions', validators = [Length(min = 0, max = 3000)])
    ingredients = TextAreaField('ingredients', validators = [Length(min = 0, max = 3000)])
    notes = TextAreaField('notes', validators = [Length(min = 0, max = 3000)])
    url = TextField('recipe_url', 
        validators = [URL(require_tld=False, message="Invalid URL"), Optional()])
    tags = QuerySelectMultipleField(
            query_factory= lambda: Tag.query.all(),
            get_label=lambda a: a.tag_name,
            widget=widgets.ListWidget(prefix_label=False),
            option_widget=widgets.CheckboxInput()
            )
        
    image_path = TextField('recipe_name')
    was_cooked = BooleanField('was_cooked')
    rating = IntegerField('rating', validators = [NumberRange(min=1, max=5, message="Rating must be between 1 and 5"), Optional()])

