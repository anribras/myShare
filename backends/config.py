class Base(object):
    URL_PREFIX = '/api/v1'


class Development(Base):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///./app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_DEBUG = True
