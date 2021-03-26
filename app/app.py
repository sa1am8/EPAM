from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
import os
import sys
sys.path.insert(1, '/home/toshka/PycharmProjects/EPAM linux/EPAM')
from instance.config import Config
from flask_script import Manager
from flask_login import LoginManager

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates/')
static_path = os.path.join(project_root, 'static/')

app = Flask(__name__, instance_relative_config=True, template_folder=template_path, static_folder=static_path)
app.config.from_object(Config)
app.config.from_pyfile('/home/toshka/PycharmProjects/EPAM linux/EPAM/instance/config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
ma = Marshmallow(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from main import main
app.register_blueprint(main)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == "__main__":
    import sys

    sys.path.insert(1, '/home/toshka/PycharmProjects/EPAM linux/EPAM')
    from models.models import *
    from models.profile import prf
    from api.views import api
    from api.auth import auth
    from flask_login import LoginManager

    db.init_app(app)

    app.register_blueprint(api)
    app.register_blueprint(auth)
    app.register_blueprint(prf)

    app.run(debug=True)
