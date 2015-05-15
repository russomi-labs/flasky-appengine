""" configuration defaults based on environment """

import logging

import os

"""
Any sensitive config items must be sourced from os.environ to avoid
checking them into source control
"""

basedir = os.path.abspath(os.path.dirname(__file__))
logging.debug('basedir: {msg}'.format(msg=basedir))

SERVER_SOFTWARE = os.getenv('SERVER_SOFTWARE', '')

is_deployed = bool(SERVER_SOFTWARE.startswith('Google App Engine'))
logging.debug('is_deployed: {msg}'.format(msg=is_deployed))

is_local = bool(SERVER_SOFTWARE.startswith('Development'))
logging.debug('is_local: {msg}'.format(msg=is_local))

is_google_appengine = bool(is_deployed or is_local)
logging.debug('is_google_appengine: {msg}'.format(msg=is_google_appengine))

APP_ENGINE_SDK_PATH = os.getenv('APP_ENGINE_SDK_PATH', '') or '~/google-cloud-sdk/platform/google_appengine'
logging.debug('APP_ENGINE_SDK_PATH: {msg}'.format(msg=APP_ENGINE_SDK_PATH))


# noinspection PyClassHasNoInit
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin <flasky@example.com>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass


# noinspection PyClassHasNoInit
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/flasky_dev'
    MAIL_USE_GAE = True
    FLASKY_MAIL_SENDER = 'russomi.dev.email@gmail.com'


# noinspection PyClassHasNoInit
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/flasky_appengine_test'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost:5000'
    MAIL_USE_GAE = True


# noinspection PyClassHasNoInit
class ProductionConfig(Config):
    MAIL_USE_GAE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'mysql+mysqldb://root@/flasky_appengine_production?unix_socket=/cloudsql/russomi-apps:production'

    # @classmethod
    # def init_app(cls, app):
    #     Config.init_app(app)
    #
    #     # email errors to the administrators
    #     import logging
    #     from logging.handlers import SMTPHandler
    #
    #     credentials = None
    #     secure = None
    #     if getattr(cls, 'MAIL_USERNAME', None) is not None:
    #         credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
    #         if getattr(cls, 'MAIL_USE_TLS', None):
    #             secure = ()
    #     mail_handler = SMTPHandler(
    #         mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
    #         fromaddr=cls.FLASKY_MAIL_SENDER,
    #         toaddrs=[cls.FLASKY_ADMIN],
    #         subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
    #         credentials=credentials,
    #         secure=secure)
    #     mail_handler.setLevel(logging.ERROR)
    #     app.logger.addHandler(mail_handler)


# noinspection PyClassHasNoInit
class HerokuConfig(ProductionConfig):
    SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle proxy server headers
        from werkzeug.contrib.fixers import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler

        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


# noinspection PyClassHasNoInit
class UnixConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to syslog
        import logging
        from logging.handlers import SysLogHandler

        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'unix': UnixConfig,

    'default': DevelopmentConfig
}
