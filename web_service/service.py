from flask import Flask
from config import Development
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from web_service.blueprints.public_api import bp as public_bp
from web_service.blueprints.page import bp as page_bp
from web_service.model.mariadb import db


app = Flask(__name__)
app.config.from_object(Development)
prefix = app.config['URL_PREFIX']
# create blueprint
app.register_blueprint(public_bp, url_prefix=prefix + '/public')
app.register_blueprint(page_bp)
db.init_app(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

