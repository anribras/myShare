class Base(object):
    URL_PREFIX = '/api/v1'


class Development(Base):
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///./app.db'
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/MosiDemo'
    SQLALCHEMY_DATABASE_URI = 'postgres://default:secret@localhost:5432/default'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    FLASK_DEBUG = True
