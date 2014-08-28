from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, RecipeForm
from models import User, ROLE_USER, ROLE_ADMIN, Recipe
from datetime import datetime
from config import RECIPES_PER_PAGE, OUR_RECIPES, MOMS_RECIPES, MEAL_IDEAS
from sqlalchemy import and_, or_

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


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
@login_required
def index(page = 1):
    recipes = Recipe.query.filter(Recipe.user_id.in_((1,3)))
    recipes = recipes.paginate(page, RECIPES_PER_PAGE, False)
    flash('Loading Recipes')
    return render_template('index.html',
        title = 'Home',
        recipes = recipes,
        url_base = 'index'
        )

@app.route('/our_recipes/', methods = ['GET', 'POST'])
@app.route('/our_recipes/<int:page>', methods = ['GET', 'POST'])
@login_required
def our_recipes( page=1 ):
    recipes = Recipe.query.filter(Recipe.user_id.in_((1,3)))
    recipes = recipes.filter('was_cooked=1')
    
    recipes = recipes.paginate(page, RECIPES_PER_PAGE, False)
    flash('Loading Recipes')
    return render_template('index.html',
        title = 'Our Recipes',
        recipes = recipes,
        url_base = 'our_recipes'
        )
    
    
@app.route('/moms_recipes/', methods = ['GET', 'POST'])
@app.route('/moms_recipes/<int:page>', methods = ['GET', 'POST'])
def moms_recipes( page=1 ):
    recipes = Recipe.query.filter(Recipe.user_id.in_((2,10)))        
    recipes = recipes.paginate(page, RECIPES_PER_PAGE, False)
    flash('Loading Recipes')
    return render_template('index.html',
        title = 'Moms Recipes',
        recipes = recipes,
        url_base = 'moms_recipes'
        )   

@app.route('/meal_ideas/', methods = ['GET', 'POST'])
@app.route('/meal_ideas/<int:page>', methods = ['GET', 'POST'])
def meal_ideas( page=1 ):
    recipes = Recipe.query.filter(Recipe.user_id.in_((1,3)))
    recipes = recipes.filter('was_cooked=0')
    recipes = recipes.paginate(page, RECIPES_PER_PAGE, False)
    flash('Loading Recipes')
    return render_template('index.html',
        title = 'Meal Ideas',
        recipes = recipes,
        url_base = 'meal_ideas'
        )  
        
@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
    return render_template('login.html', 
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])

@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname = nickname, email = resp.email, role = ROLE_USER)
        db.session.add(user)
        db.session.commit()
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page = 1):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    return render_template('user.html',
        user = user,
        posts = posts)


@app.route('/add_recipe/',methods = ['GET', 'POST']) 
@app.route('/add_recipe/<source_url>',methods = ['GET']) 
@login_required
def add_recipe(source_url = None):
    form = RecipeForm(request.form)
    
    flash(source_url)
    print request.method
    if request.method == "POST":
        recipe = Recipe()
        if form.validate_on_submit():
            form.populate_obj(recipe)
            db.session.add(recipe)
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('add_recipe'))
        else:
            return render_template('add_recipe.html',form = form)
    elif request.method != "POST":
        if source_url != None:
            print "Source"
            print source_url
        return render_template('add_recipe.html',form = form)
    return redirect(url_for('add_recipe'))

@app.route('/edit_recipe/<id>', methods = ['GET', 'POST'])
@login_required
def edit_recipe(id=1):
    recipe = Recipe.query.filter_by(id = id).first()
    form = RecipeForm(obj = recipe)
    if recipe == None:
        flash('Recipe not found.')
        return redirect(url_for('index'))
    if form.validate_on_submit():
        form.populate_obj(recipe)
        db.session.add(recipe)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_recipe', id=id))
    return render_template('edit_recipe.html',
        form = form)

@app.route('/view_recipe/<id>',methods = ['GET', 'POST']) 
@login_required
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
@login_required
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
@login_required
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
        
    