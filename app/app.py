from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate, MigrateCommand
from config import config
from flask_script import Manager
import os



project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates/')

db = SQLAlchemy()
app = Flask(__name__, instance_relative_config=True, template_folder=template_path)
app.config.from_object(config)
app.config.from_object("config")
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
ma = Marshmallow(app)
