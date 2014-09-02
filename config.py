import os


basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    DEBUG = False
    TESTING = False
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

    CSRF_ENABLED = True
    SECRET_KEY = '%@#$%$^@ASDF'

    RECIPES_PER_PAGE = 10
    RECIPES_PER_HOME_PAGE = 5

    UPLOADS_DEFAULT_DEST = 'app/static/pictures/'
    TEMP_FILE = 'temp.jpg'
    IMAGE_SIZE = (640,480)
    ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
    
 
class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = True

