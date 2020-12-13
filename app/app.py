from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
import os
import sys
sys.path.insert(1, '/home/toshka/PycharmProjects/EPAM linux/EPAM')
from instance.config import Config
from flask_script import Manager

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates/')

db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=True, template_folder=template_path)
app.config.from_object(Config)
app.config.from_pyfile('/home/toshka/PycharmProjects/EPAM linux/EPAM/instance/config.py')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
ma = Marshmallow(app)


if __name__ == '__main__' or __name__ == 'flask_test.py':
    import sys
    sys.path.insert(1, '/home/toshka/PycharmProjects/EPAM linux/EPAM')
    from models.empl import emp
    from models.models import *
    from main import main
    from models.dep import dep
    from api.views import api

    app.register_blueprint(main)
    app.register_blueprint(emp)
    app.register_blueprint(dep)
    app.register_blueprint(api)

    app.run(debug=True)
