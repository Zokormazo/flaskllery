# coding=utf8
"""
Copyright 2014, Julen Landa Alustiza

Licensed under the Eiffel Forum License 2.
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # flask-wtf
    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'This is an insecure secret key'

    # flask-mail
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = '587'
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = 'no-reply@flask'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    # flask-user
    USER_ENABLE_EMAIL = True
    USER_ENABLE_CHANGE_USERNAME = False
    USER_ENABLE_REGISTRATION = True
    USER_ENABLE_USERNAME = True
    USER_APP_NAME = 'Flaskllery'

    # administrator list
    ADMINS = os.environ.get('ADMINS')

    LANGUAGES = {
            'en': 'English',
            'eu': 'Euskara'
    }

    #Flaskllery

    FLASKLLERY_ALBUMS_PER_PAGE = 6
    FLASKLLERY_PHOTOS_PER_PAGE = 12
    FLASKLLERY_USERS_PER_PAGE = 20
    FLASKLLERY_CACHE_DIR = os.path.join(basedir, 'cache/')
    FLASKLLERY_MAIL_SUBJECT_PREFIX = '[Flaskllery]'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'db/data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'db/data-test.sqlite')
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'db/data.sqlite')

    @classmethod
    def init_app(self, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(self, 'MAIL_USERNAME', None) is not None:
            credentials = (self.MAIL_USERNAME, self.MAIL_PASSWORD)
        if getattr(self, 'MAIL_USE_TLS', None):
            secure = ()
        mail_handler = SMTPHandler(
                mailhost=(self.MAIL_SERVER, self.MAIL_PORT),
                fromaddr=self.MAIL_DEFAULT_SENDER,
                toaddrs=[self.ADMINS],
                subject=self.FLASKLLERY_MAIL_SUBJECT_PREFIX + ' Application Error',
                credentials=credentials,
                secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,

        'default': DevelopmentConfig
}
