import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import basedir
from werkzeug import secure_filename

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)


from app import views, models

@app.template_filter()
def datetimefilter(value, format='%B %Y'):
    """convert a datetime to a different format."""
    return value.strftime(format)

app.jinja_env.filters['datetimefilter'] = datetimefilter

if app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/recipe.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d] [%(funcName)s function]'))
    log_level = logging.DEBUG
    app.logger.setLevel(log_level)
    file_handler.setLevel(log_level)
    app.logger.addHandler(file_handler)
    app.logger.info('Starting Recipes')




