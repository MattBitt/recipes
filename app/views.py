from flask import render_template, flash, redirect, session, url_for, request, g
from app import app, db
from forms import RecipeForm
from models import Recipe
from datetime import datetime, date
from sqlalchemy import desc
from scraper import scrape_recipe
import random
import os
from image_functions import resize_picture
import random

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
    recent_recipes = get_recent_recipes().limit(5).all()
    #favorite_recipes = get_favorite_recipes().all()
    for r in recent_recipes:
        r.fav = False
    my_recipes = set(recent_recipes)
    
    while len(my_recipes) < 10:
        favorite = get_favorites()
        for fav in favorite:
            fav.fav  = True
            my_recipes.add(fav)
            if len(my_recipes) == 10:
                break
        
    #need to check if any random are in recent_recipes.  if they are get a new one
    my_recipes = list(my_recipes)
    random.shuffle(my_recipes)

    return render_template('index.html',
        title = 'Home',
        recipes = my_recipes, 
        single_page = True,
         url_base = 'index'
        )

@app.route('/our_recipes/', methods = ['GET', 'POST'])
@app.route('/our_recipes/<int:page>', methods = ['GET', 'POST'])
def our_recipes( page=1 ):
    recipes = Recipe.query.filter(Recipe.user_id.in_((1,3))).filter('was_cooked=1').order_by(Recipe.recipe_name)
    single_page = not recipes.count() > app.config['RECIPES_PER_PAGE']
    if not single_page:
        recipes = recipes.paginate(page, app.config['RECIPES_PER_PAGE'], False)
    else:
        recipes = recipes.all()

    return render_template('index.html',
        title = 'Our Cookbook',
        recipes = recipes,
        single_page = single_page,
        url_base = 'our_recipes'
        )
    
    
@app.route('/moms_recipes/', methods = ['GET', 'POST'])
@app.route('/moms_recipes/<int:page>', methods = ['GET', 'POST'])
def moms_recipes( page=1 ):
    recipes = Recipe.query.filter('user_id=3').order_by(Recipe.recipe_name)        
    single_page = not recipes.count() > app.config['RECIPES_PER_PAGE']
    if not single_page:
        recipes = recipes.paginate(page, app.config['RECIPES_PER_PAGE'], False)
    else:
        recipes = recipes.all()
    return render_template('index.html',
        title = 'Moms Recipes',
        recipes = recipes,
        single_page = single_page,
        url_base = 'moms_recipes'
        )   

@app.route('/meal_ideas/', methods = ['GET', 'POST'])
@app.route('/meal_ideas/<int:page>', methods = ['GET', 'POST'])
def meal_ideas( page=1 ):
    recipes = Recipe.query.filter(Recipe.user_id.in_((1,3))).filter('was_cooked=0').order_by(Recipe.recipe_name)
    single_page = not recipes.count() > app.config['RECIPES_PER_PAGE']
    if not single_page:
        recipes = recipes.paginate(page, app.config['RECIPES_PER_PAGE'], False)
    else:
        recipes = recipes.all()
    


    return render_template('index.html',
        title = 'Meal Ideas',
        recipes = recipes,
        single_page = single_page,
        url_base = 'meal_ideas'
        )  
        
        
        
@app.route('/add_recipe/',methods = ['GET', 'POST']) 
def add_recipe():
    if request.query_string[:4] == "url=":
       app.logger.info("Adding from source:  " + request.query_string[4:])
       form = fillout_form( request.query_string[4:] )
    else:
        form = RecipeForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            app.logger.info("Adding a new Recipe")
            recipe=Recipe()
            form.populate_obj(recipe)
            if len(request.files) > 0:
                app.logger.debug("Image uploaded")
                req = request
                filename = req.files['image_file'].filename
                recipe_name = recipe.recipe_name
                recipe.image_path = upload_image(req, filename, recipe_name)
                if recipe.image_path is None:
                    flash("Error uploading image")
            recipe.user_id = 1
            recipe.timestamp = date.today()
            db.session.add(recipe)
            db.session.commit()
            
            new_rec = Recipe.query.filter(Recipe.recipe_name==  str(recipe.recipe_name)).first()
            #import pdb; pdb.set_trace()
            return redirect(url_for('view_recipe', id=new_rec.id))
        else:
            flash('Invalid data')
            return render_template('recipe_form.html',form = form)
    elif request.method != "POST":
        return render_template('recipe_form.html',form = form)
    return redirect(url_for('add_recipe'))

@app.route('/edit_recipe/<id>', methods = ['GET', 'POST'])
def edit_recipe(id=1):
    recipe = Recipe.query.filter_by(id = id).first()
    app.logger.info('Editing Recipe ' + str(id))
    form = RecipeForm(obj = recipe)
    if recipe == None:
        flash('Recipe not found.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        app.logger.debug('request.data')
        app.logger.debug(request.data)
        app.logger.debug('Method = POST')
        valid = form.validate_on_submit()
        if valid:
            app.logger.info('Validation Successful - ' + str(form.recipe_name.data))
            form.populate_obj(recipe)
            if len(request.files) > 0 and request.files['image_file'].filename:
                req = request
                filename = req.files['image_file'].filename
                recipe_name = recipe.recipe_name
                recipe.image_path = upload_image(req, filename, recipe_name)
                if recipe.image_path is None:
                    app.logger.error('Error uploading image')
                    flash("Error uploading image")
                
            db.session.add(recipe)
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('view_recipe', id=id))
        else:
            app.logger.info("Failed Validation")
            import pdb; pdb.set_trace()        
    return render_template('recipe_form.html',
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

def get_recent_recipes():
    return Recipe.query.filter(
               Recipe.user_id.in_((1,2))).filter(
               'was_cooked=1').order_by(desc(Recipe.timestamp))

        
# def get_favorite_recipes():        
    # favorite_recipes = Recipe.query.filter('rating=5')
    # random_favs = []
    # while len(random_favs) < app.config['RECIPES_PER_HOME_PAGE']:
        # random_row = int(favorite_recipes.count()*random.random())
        # if random_row not in random_favs:
            # random_favs.append(random_row)
    # random_fav_ids = []
    # for f in random_favs:
        # random_fav_ids.append(favorite_recipes[f].id)
    # favorite_recipes = Recipe.query.filter(Recipe.id.in_(random_fav_ids))
    # return favorite_recipes
    
def upload_image( req, filename, recipe_name ):
        """
        Check for empty filename before calling this function.
        
        """
        dest_path = app.config['UPLOADS_DEFAULT_DEST']
        temp_file = app.config['TEMP_FILE']
        fname, ext = os.path.splitext(filename)
        temp_path = os.path.join(dest_path, temp_file)
        req.files['image_file'].save(temp_path)
        resized_pic = resize_picture(dest_path, 
                temp_file, 
                str(recipe_name) + ext,
                (app.config['IMAGE_SIZE']))
        if resized_pic:
            return str(recipe_name) + ext
        else:
            os.remove(os.path.join(dest_path, temp_file))
            return None
         
def get_css_props( index ):
    css_props = {'class':'img' + str(index + 1)}
    css_props['tilt'] = random.randint(-10, 10)
    return css_props
    
def get_favorites():
    favorite_recipes = Recipe.query.filter('rating=5').all()
    random.shuffle(favorite_recipes)
    return favorite_recipes[0:5]