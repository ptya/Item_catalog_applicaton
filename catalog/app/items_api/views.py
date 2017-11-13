#!/usr/bin/env python3
# -*- coding: latin-1 -*-

from flask import Blueprint, jsonify

from app import app, session
from app.models import Item, Category

#
# Config
#

items_api_blueprint = Blueprint('items_api', __name__)


#
# Routes
#

# List all categories
@items_api_blueprint.route('/catalog/categories/JSON')
def categoriesJSON():
    cats = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in cats])


# List all items for given category
@items_api_blueprint.route('/catalog/<category_name>/items/JSON')
def itemsJSON(category_name):
    items = session.query(Item).filter_by(category=category_name).all()
    return jsonify(items=[i.serialize for i in items])


# List item information
@items_api_blueprint.route('/catalog/<category_name>/<item_name>/JSON')
def itemJSON(category_name, item_name):
    item_name = item_name.replace('+', ' ')
    item = session.query(Item).filter_by(name=item_name).first()
    return jsonify(item=[item.serialize])
