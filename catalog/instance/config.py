#!/usr/bin/env python3
# -*- coding: latin-1 -*-

import os
import json
import random
import string

# Top-level directory
BASEDIR = os.path.abspath(os.path.dirname(__file__))
TOP_LEVEL_DIR = os.path.abspath(os.curdir)

# Generl app config
SECRET_KEY = ''.join(
    random.choice(string.ascii_uppercase + string.digits) for x in range(32))
DEBUG = True

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:////%s/db/item_catalog.db' % TOP_LEVEL_DIR

# OAUTH JSON files
GOO_CLIENT_ID = json.loads(
    open('./instance/goo_client_secret.json', 'r')
    .read())['web']['client_id']

GH_CLIENT_ID = json.loads(
    open('./instance/gh_client_secret.json', 'r')
    .read())['web']['client_id']

GH_SECRET = json.loads(
    open('./instance/gh_client_secret.json', 'r')
    .read())['web']['client_secret']

FB_CLIENT_ID = json.loads(
    open('./instance/fb_client_secret.json', 'r')
    .read())['web']['app_id']

FB_SECRET = json.loads(
    open('./instance/fb_client_secret.json', 'r')
    .read())['web']['app_secret']

# Uploads
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = '%s/app/static/images/uploaded/' % TOP_LEVEL_DIR
MAX_CONTENT_LENGTH = 4 * 1024 * 1024
