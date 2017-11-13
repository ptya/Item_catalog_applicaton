#!/usr/bin/env python3
# -*- coding: latin-1 -*-

from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required
from sqlalchemy import desc
from werkzeug.utils import secure_filename

import random
import string
import bleach
import os

from app import app, session
from app.models import Item, Category

#
# Config
#

items_blueprint = Blueprint('items', __name__)


#
# Helper functions
#

def allowed_file(filename):
    """Returns true if the file extension is okay"""
    return ('.' in filename and filename.rsplit('.', 1)[1].lower()
            in app.config['ALLOWED_EXTENSIONS'])


#
# Routes
#

@items_blueprint.route('/')
@items_blueprint.route('/catalog')
def showHome():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(desc(Item.id)).limit(len(categories))
    if current_user.is_authenticated:
        return render_template('home.html', categories=categories,
                               items=items)
    else:
        return render_template('publichome.html', categories=categories,
                               items=items)


@items_blueprint.route('/catalog/<category_name>/items')
def showItems(category_name):
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category=category_name).all()
    if current_user.is_authenticated:
        return render_template('items.html', categories=categories,
                               items=items, name=category_name)
    else:
        return render_template('publicitems.html', categories=categories,
                               items=items, name=category_name)


@items_blueprint.route('/catalog/<category_name>/<item_name>')
def showDescription(category_name, item_name):
    item_name = item_name.replace('+', ' ')
    item = session.query(Item).filter_by(name=item_name).first()
    if current_user.is_authenticated:
        return render_template('description.html', item=item)
    else:
        return render_template('publicdescription.html', item=item)


@items_blueprint.route('/catalog/new', methods=['GET', 'POST'])
@login_required
def newItem(cat=None):
    if request.method == 'GET':
        if request.args.get('cat'):
            cat = request.args.get('cat')
        categories = session.query(Category).order_by(Category.name).all()
        return render_template('newitem.html', categories=categories, cat=cat)
    if request.method == 'POST':
        # if file is not part of the request something is fishy
        if 'file' not in request.files:
            return redirect(url_for('items.newItem'))
        file = request.files['file']
        # clean filename for possible mischief
        filename = secure_filename(file.filename)
        if file and filename != '' and allowed_file(filename):
            # add hash folder for overwrite safety
            dirname = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for x in range(8))
            path = os.path.join(app.config['UPLOAD_FOLDER'], dirname,
                                filename)
            if not os.path.exists(os.path.dirname(path)):
                try:
                    os.makedirs(os.path.dirname(path))
                # Guard against race condition
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            file.save(path)
            # update filename to store in db
            filename = '%s/%s' % (dirname, filename)

        newItem = Item(name=bleach.clean(request.form['title']),
                       description=bleach.clean(request.form['desc']),
                       category=bleach.clean(request.form['cat']),
                       image=filename)
        session.add(newItem)
        session.commit()
        flash('Item created.', 'success')
        return redirect(url_for('items.showHome'))


@items_blueprint.route('/catalog/<item_name>/edit', methods=['GET', 'POST'])
@login_required
def editItem(item_name):
    item_name = item_name.replace('+', ' ')
    edited_item = session.query(Item).filter_by(name=item_name).first()
    if request.method == 'GET':
        categories = session.query(Category).order_by(Category.name).all()
        return render_template('edititem.html', item=edited_item,
                               categories=categories)
    if request.method == 'POST':
        # if file is not part of the request something is fishy
        if 'file' not in request.files:
            return redirect(url_for('items.editItem', item_name=item_name))
        file = request.files['file']
        # clean filename for possible mischief
        filename = secure_filename(file.filename)
        if file and filename != '' and allowed_file(filename):
            # add hash folder for overwrite safety
            dirname = ''.join(random.choice(
                string.ascii_uppercase + string.digits) for x in range(8))
            path = os.path.join(app.config['UPLOAD_FOLDER'], dirname,
                                filename)
            if not os.path.exists(os.path.dirname(path)):
                try:
                    os.makedirs(os.path.dirname(path))
                # Guard against race condition
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise
            file.save(path)
            # update filename to store in db
            filename = '%s/%s' % (dirname, filename)
            # delete previous image if there was
            if edited_item.image != None:
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'],
                                       edited_item.image))
                prev_dirname = edited_item.image.split('/')[0]
                os.rmdir(os.path.join(app.config['UPLOAD_FOLDER'],
                                      prev_dirname))

        edited_item.name = bleach.clean(request.form['title'])
        edited_item.description = bleach.clean(request.form['desc'])
        edited_item.category = bleach.clean(request.form['cat'])
        if filename != '':
            edited_item.image = filename
        session.add(edited_item)
        session.commit()
        flash('Item updated.', 'success')
        return render_template('description.html', item=edited_item)


@items_blueprint.route('/catalog/<item_name>/delete', methods=['GET', 'POST'])
@login_required
def deleteItem(item_name):
    item_name = item_name.replace('+', ' ')
    deleted_item = session.query(Item).filter_by(name=item_name).first()
    if request.method == 'GET':
        return render_template('deleteitem.html', item=deleted_item)
    if request.method == 'POST':
        session.delete(deleted_item)
        session.commit()
        # delete image if there was
        if deleted_item.image != '':
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'],
                                   deleted_item.image))
            prev_dirname = deleted_item.image.split('/')[0]
            os.rmdir(os.path.join(app.config['UPLOAD_FOLDER'],
                                  prev_dirname))
        flash('Item deleted.', 'success')
        return redirect(url_for('items.showHome'))
