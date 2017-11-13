#!/usr/bin/env python3
# -*- coding: latin-1 -*-

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from app.models import Base, User


#
# Config
#

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

csrf = CSRFProtect(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Login manager setup to load the user from the database
@login_manager.user_loader
def load_user(user_id):
    try:
        user = session.query(User).filter_by(id=user_id).one()
        return user
    except exc.SQLAlchemyError:
        return None


#
# Blueprints
#

from app.users.views import users_blueprint  # noqa
from app.items.views import items_blueprint  # noqa
from app.items_api.views import items_api_blueprint  # noqa

# register the blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(items_blueprint)
app.register_blueprint(items_api_blueprint)
