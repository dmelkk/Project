import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ADMIN = os.environ.get('ADMIN') or 'dmelkk@gmail.com'
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHMEY_TRACK_MODIFICATION = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'default'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'default'
    POSTS_PER_PAGE = 5
    COMMENTS_PER_PAGE = 10

    @staticmethod
    def init_app(app):
        pass
        

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
            'sqlite:///' + os.path.join(basedir, 'data.sqlite')


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI') or \
            'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


config = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,

        'default': DevelopmentConfig
        }
