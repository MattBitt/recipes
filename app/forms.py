from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length
from app.models import User

class LoginForm(Form):
    openid = TextField('openid', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)
    
class EditForm(Form):
    nickname = TextField('nickname', validators = [DataRequired()])
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])
    
    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname
        
    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True
        
class PostForm(Form):
    post = TextField('post', validators = [DataRequired()])
    
class AddRecipeForm(Form):
    recipe_name = TextField('recipe_name', validators = [DataRequired()])
    directions = TextAreaField('directions', validators = [Length(min = 0, max = 140)])
    ingredients = TextAreaField('ingredients', validators = [Length(min = 0, max = 140)])
    notes = TextAreaField('notes', validators = [Length(min = 0, max = 140)])
    url = TextField('recipe_name')
    image_path = TextField('recipe_name')
    was_cooked = BooleanField('was_cooked')
    rating = IntegerField('rating')

