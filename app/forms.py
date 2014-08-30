from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, TextAreaField, IntegerField, widgets, DateTimeField, FileField
from wtforms import SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, URL, Optional, NumberRange, Email
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from app.models import User, Recipe
from app import db



class SignupForm(Form):
  name = TextField("First name",  validators = [DataRequired("Please enter your first name.")])
  email = TextField("Email",  validators = [DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators = [DataRequired("Please enter a password.")])
  submit = SubmitField("Create account")
 
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user:
      self.email.errors.append("That email is already taken")
      return False
    else:
      return True

class SigninForm(Form):
  email = TextField("Email", validators = [DataRequired("Please enter your email address."), Email("Please enter your email address.")])
  password = PasswordField('Password', validators = [DataRequired("Please enter a password.")])
  submit = SubmitField("Sign In")
   
  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(email = self.email.data.lower()).first()
    if user and user.check_password(self.password.data):
      return True
    else:
      self.email.errors.append("Invalid e-mail or password")
      return False






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
    image_path = TextField('image_path')
    was_cooked = BooleanField('was_cooked')
    rating = IntegerField('rating', validators = [NumberRange(min=1, max=5, message="Rating must be between 1 and 5"), Optional()])
    user_id = IntegerField('user_id')
    timestamp = DateTimeField('timestamp')
    image_file = FileField()
    
    
