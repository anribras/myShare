from flask import Flask
from backends.config import Development
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from backends.blueprints.public_api import bp as public_bp
from backends.blueprints.page import bp as page_bp
from backends.model.mariadb import db
from flask_cors import CORS


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


CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
