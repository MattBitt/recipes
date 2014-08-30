from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from forms import RecipeForm, LoginForm
from models import User, Recipe, hash_pass
from datetime import datetime, date
from sqlalchemy import desc
from scraper import scrape_recipe
import random
import os

@app.route("/logout/")
def logout_page():
    """
    Web Page to Logout User, then Redirect them to Index Page.
    """
    logout_user()
    return redirect("/")
 
@app.route("/login/", methods=["GET", "POST"])
def login_page():
    """
    Web Page to Display Login Form and process form. 
    """
    form = LoginForm()
    if request.method == "POST":
        user = User.query.filter_by(user_name=request.form['user_name']).first()
 
        #If we found a user based on username then compare that the submitted
        #password matches the password in the database.  The password is stored
        #is a slated hash format, so you must hash the password before comparing
        #it.
        if user and hash_pass(request.form['password']) == user.password:
            login_user(user, remember=True)
            return redirect(request.args.get("next") or "/")        
 
    return render_template("login.html", form=form)

@app.errorhandler(404)
def internal_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
    
   
@app.route('/', methods = ['GET', 'POST'])
@app.route('/index/', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
def index(page = 1):
    #user_id = (current_user.get_id() or "No User Logged In")
    #flash(user_id)
    recent_recipes = get_recent_recipes().paginate(page, app.config['RECIPES_PER_HOME_PAGE'], False)
    favorite_recipes = get_favorite_recipes().paginate(page, app.config['RECIPES_PER_HOME_PAGE'], False)
    #flash('Loading Recipes')
    return render_template('index.html',
        title = 'Home',
        recent_recipes = recent_recipes,
        favorite_recipes = favorite_recipes,
        url_base = 'index'
        )

@app.route('/our_recipes/', methods = ['GET', 'POST'])
@app.route('/our_recipes/<int:page>', methods = ['GET', 'POST'])
def our_recipes( page=1 ):
    #user_id = (current_user.get_id() or "No User Logged In")
    recipes = Recipe.query.filter(Recipe.user_id.in_((1,3))).filter('was_cooked=1').order_by(Recipe.recipe_name)
    recipes = recipes.paginate(page, app.config['RECIPES_PER_PAGE'], False)
    #flash('Loading Recipes')
    return render_template('browse.html',
        title = 'Our Recipes',
        recipes = recipes,
        url_base = 'our_recipes'
        )
    
    
@app.route('/moms_recipes/', methods = ['GET', 'POST'])
@app.route('/moms_recipes/<int:page>', methods = ['GET', 'POST'])
def moms_recipes( page=1 ):
    recipes = Recipe.query.filter('user_id=3').order_by(Recipe.recipe_name)        
    recipes = recipes.paginate(page, app.config['RECIPES_PER_PAGE'], False)
    #flash('Loading Recipes')
    return render_template('browse.html',
        title = 'Moms Recipes',
        recipes = recipes,
        url_base = 'moms_recipes'
        )   

@app.route('/meal_ideas/', methods = ['GET', 'POST'])
@app.route('/meal_ideas/<int:page>', methods = ['GET', 'POST'])
def meal_ideas( page=1 ):
    recipes = Recipe.query.filter(Recipe.user_id.in_((1,3))).filter('was_cooked=0').order_by(Recipe.recipe_name)
    recipes = recipes.filter('was_cooked=0')
    recipes = recipes.paginate(page, app.config['RECIPES_PER_PAGE'], False)
    flash('Loading Recipes')
    return render_template('browse.html',
        title = 'Meal Ideas',
        recipes = recipes,
        url_base = 'meal_ideas'
        )  
        
        
        
@app.route('/add_recipe/',methods = ['GET', 'POST']) 
def add_recipe():
    if request.query_string[:4] == "url=":
       form = fillout_form( request.query_string[4:] )
    else:
        form = RecipeForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            save_new_recipe( form )
            flash('Your changes have been saved.')
            return redirect(url_for('add_recipe'))
        else:
            return render_template('add_recipe.html',form = form)
    elif request.method != "POST":
        return render_template('add_recipe.html',form = form)
    return redirect(url_for('add_recipe'))

@app.route('/edit_recipe/<id>', methods = ['GET', 'POST'])
def edit_recipe(id=1):
    recipe = Recipe.query.filter_by(id = id).first()
    form = RecipeForm(obj = recipe)
    if recipe == None:
        flash('Recipe not found.')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        form.populate_obj(recipe)
        if request.files['image_file'].filename != recipe.image_path:
            upload_image( recipe )
        db.session.add(recipe)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('view_recipe', id=id))
    return render_template('edit_recipe.html',
        form = form)

@app.route('/view_recipe/<id>',methods = ['GET', 'POST']) 
def view_recipe(id):
    recipe = Recipe.query.filter_by(id = id).first()
    if recipe == None:
        flash('Recipe ' + recipe['id'] + ' not found.')
        return redirect(url_for('index'))
    else:
        if recipe.ingredients != None:
            recipe.ingredient_list = recipe.ingredients.split('\n')
        if recipe.directions != None:
            recipe.direction_list = recipe.directions.split('\n')
        if recipe.notes != None:
            recipe.note_list = recipe.notes.split('\n')
    return render_template('view_recipe.html',
        recipe = recipe)

@app.route('/delete_recipe/<int:id>')

def delete_recipe(id):
    recipe = Recipe.query.filter_by(id = id).first()
    if recipe == None:
        flash('Recipe not found.')
        return redirect(url_for('index'))
    db.session.delete(recipe)
    db.session.commit()
    flash('The recipe has been deleted.')
    return redirect(url_for('index'))

@app.route('/print_recipe/<id>',methods = ['GET', 'POST']) 

def print_recipe(id):
    recipe = Recipe.query.filter_by(id = id).first()
    if recipe == None:
        flash('Recipe ' + recipe['id'] + ' not found.')
        return redirect(url_for('index'))
    else:
        if recipe.ingredients != None:
            recipe.ingredient_list = recipe.ingredients.split('\n')
        if recipe.directions != None:
            recipe.direction_list = recipe.directions.split('\n')
        if recipe.notes != None:
            recipe.note_list = recipe.notes.split('\n')
    return render_template('print_recipe.html',
        recipe = recipe)
       
def fillout_form( url ):
    #import pdb; pdb.set_trace()
    new_recipe = scrape_recipe(url)
    if new_recipe != None:
        form = RecipeForm(request.form)
        form.recipe_name.data = new_recipe.get_title()
        form.ingredients.data = new_recipe.get_ingredients()
        form.directions.data = new_recipe.get_directions()
        form.user_id.data = 1
        form.timestamp.data = date.today()
        form.url.data = url
        return form
    else:
        return None
        
def save_new_recipe( form ):                
    recipe=Recipe()
    form.populate_obj(recipe)
    if recipe.image_file != None:
        recipe.image_path = upload_image(recipe)
        recipe.user_id = 1
        recipe.timestamp = date.today()
    db.session.add(recipe)
    db.session.commit()
    
def get_recent_recipes():
    return Recipe.query.filter(
               Recipe.user_id.in_((1,2))).filter(
               'was_cooked=1').order_by(desc(Recipe.timestamp))
               
            
        
def get_favorite_recipes():        
    favorite_recipes = Recipe.query.filter('rating=5')
    random_favs = []
    while len(random_favs) < app.config['RECIPES_PER_HOME_PAGE']:
        random_row = int(favorite_recipes.count()*random.random())
        if random_row not in random_favs:
            random_favs.append(random_row)
    random_fav_ids = []
    for f in random_favs:
        random_fav_ids.append(favorite_recipes[f].id)
    favorite_recipes = Recipe.query.filter(Recipe.id.in_(random_fav_ids))
    return favorite_recipes
    
def upload_image( recipe ):
        if request.files['image_file'].filename != '':
            fname, ext = os.path.splitext(request.files['image_file'].filename)
            recipe.image_path = str(recipe.recipe_name) + '.' + ext
            request.files['image_file'].save(app.config['UPLOADS_DEFAULT_DEST'] + str(recipe.image_path))
            return recipe.image_path
         
    
    
