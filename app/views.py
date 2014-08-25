from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from forms import LoginForm, EditForm, PostForm, AddRecipeForm
from models import User, ROLE_USER, ROLE_ADMIN, Recipe
from datetime import datetime
from config import POSTS_PER_PAGE

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
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page = 1):
    recipes = [
        { 
            'recipe_name': 'Tacos', 
            'url' : 'www.food.com',
            'was_cooked' : 0,
            'rating' : 11
        },
        { 
            'recipe_name': 'Burritos', 
            'url' : 'www.foodnetwork.com',
            'was_cooked' : 1,
            'rating' : 9
        },
        { 
            'recipe_name': 'Boudin', 
            'url' : 'www.foodnetwork.com',
            'was_cooked' : 1,
            'rating' : 9
        },
        { 
            'recipe_name': 'Catfish', 
            'url' : 'www.foodnetwork.com',
            'was_cooked' : 1,
            'rating' : 9
        }
    ]
    
    flash('Loading Recipes')
    return render_template('index.html',
        title = 'Home',
        recipes = recipes)

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
        # make the user follow him/herself
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
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html',
        user = user,
        posts = posts)

@app.route('/edit', methods = ['GET', 'POST'])
@login_required
def edit():
    form = EditForm(g.user.nickname)
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    elif request.method != "POST":
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html',
        form = form)


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post == None:
        flash('Post not found.')
        return redirect(url_for('index'))
    if post.author.id != g.user.id:
        flash('You cannot delete this post.')
        return redirect(url_for('index'))
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.')
    return redirect(url_for('index'))

    
@app.route('/add_recipe',methods = ['GET', 'POST']) 
@app.route('/add_recipe/<source>',methods = ['GET', 'POST']) 
@login_required
def add_recipe(source = None):
    form = AddRecipeForm(request.form)
    print request.method
    if request.method == "POST":
        if form.validate_on_submit():
            recipe = Recipe(recipe_name=form.recipe_name.data, 
                directions=form.directions.data,
                ingredients=form.ingredients.data,
                notes = form.notes.data,
                url = form.url.data,
                user_id = g.user.nickname,
                image_path = form.image_path.data,
                rating = form.rating.data,
                timestamp = datetime.now(),
                was_cooked = form.was_cooked.data)
            db.session.add(recipe)
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('add_recipe'))
        else:
            return render_template('add_recipe.html',form = form)
    elif request.method != "POST":
        #form.recipe_name.data = g.user.nickname
        print "Second condition"
        return render_template('add_recipe.html',form = form)
    
    print "Final"
    return redirect(url_for('add_recipe'))
    