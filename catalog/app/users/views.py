#!/usr/bin/env python3
# -*- coding: latin-1 -*-

from flask import Blueprint, render_template, url_for, redirect, request
from flask import make_response, flash
from flask import session as login_session
from flask_login import login_required, login_user, logout_user
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

import random
import json
import string
import requests

from app import app, session
from app.models import User

#
# Config
#

users_blueprint = Blueprint('users', __name__)


#
# Helper functions
#

# User related database functions
def createUser(login_session):
    """Create a user in database and return the id"""
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserID(email):
    """Return user_id from database based on email recieved"""
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def getUserInfo(user_id):
    """Return User object based on user_id"""
    try:
        user = session.query(User).filter_by(id=user_id).one()
        return user
    except exc.SQLAlchemyError:
        return None


def getUser(login_session):
    """Return user_id based on login_session info"""
    # check if user exists, if not create a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    return user_id


# Disconnect functions
def gdisconnect():
    """Disconnect from Google and remove related session info"""
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke'
    params = {'token': access_token}
    data = requests.get(url, params=params)
    if data.status_code == '200':
        # Reset user session
        del login_session['gplus_id']
        return True
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


def fbdisconnect():
    """Disconnect from Facebook and remove related session info"""
    facebook_id = login_session['facebook_id']
    token = login_session['credentials']
    url = 'https://graph.facebook.com/%s/permissions' % facebook_id
    params = {'access_token': token}
    data = requests.delete(url, params=params)
    result = data.json()
    if result['success']:
        del login_session['facebook_id']
        return True
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


def ghdisconnect():
    """Disconnect from Github and remove related session info"""
    del login_session['github_id']
    return True

#
# Routes
#


@users_blueprint.route('/login')
def showLogin():
    state = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state,
                           GOO_ID=app.config['GOO_CLIENT_ID'],
                           FB_ID=app.config['FB_CLIENT_ID'],
                           GH_ID=app.config['GH_CLIENT_ID'])


@users_blueprint.route('/login_success')
def loginSuccess():
    return render_template('loginsuccess.html')


@users_blueprint.route('/gconnect', methods=['POST'])
def gconnect():
    # Check if state matches
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    # Exchange tokens
    try:
        oauth_flow = flow_from_clientsecrets(
            './instance/goo_client_secret.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token

    # Grab tokeninfo
    url = 'https://www.googleapis.com/oauth2/v2/tokeninfo'
    params = {'access_token': access_token}
    data = requests.get(url, params=params)
    result = data.json()

    # Check for errors ans fishy stuff
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != app.config['GOO_CLIENT_ID']:
        response = make_response(
            json.dumps("Token's client ID does not match app's"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

    # Store info in session
    login_session['provider'] = 'google'
    login_session['credentials'] = access_token
    login_session['gplus_id'] = gplus_id

    # Grab user info and store it
    url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    params = {'access_token': access_token,
              'alt': 'json'}
    data = requests.get(url, params=params)
    result = data.json()

    login_session['username'] = result['name']
    # sometimes there's no picture so have a default one
    if result['picture'] == '':
        login_session['picture'] = url_for(
            'static', filename='images/default/user_default.png')
    else:
        login_session['picture'] = result['picture']
    login_session['email'] = result['email']

    # check if user exists, if not create a new one
    u_id = getUser(login_session)
    user = session.query(User).filter_by(id=u_id).one()
    login_user(user)
    return 'Login successful'


@users_blueprint.route('/fbconnect', methods=['POST'])
def fbconnect():
    # Check if state matches
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data

    # Exchanging client token for server-side token
    url = 'https://graph.facebook.com/oauth/access_token'
    params = {'grant_type': 'fb_exchange_token',
              'client_id': app.config['FB_CLIENT_ID'],
              'client_secret': app.config['FB_SECRET'],
              'fb_exchange_token': access_token}
    data = requests.get(url, params=params)
    result = data.json()

    # Use token to get user info from API
    userinfo_url = 'https://graph.facebook.com/v2.10/me'
    token = result['access_token']
    params = {'fields': 'id,email,name',
              'access_token': token}
    data = requests.get(userinfo_url, params=params)
    result = data.json()
    login_session['provider'] = 'facebook'
    login_session['username'] = result['name']
    login_session['email'] = result['email']
    login_session['facebook_id'] = result['id']
    login_session['credentials'] = token

    # Get user picture
    url = '%s/picture' % userinfo_url
    params = {'redirect': 0,
              'height': 200,
              'width': 200,
              'access_token': token}
    data = requests.get(url, params=params)
    result = data.json()
    login_session['picture'] = result['data']['url']

    # check if user exists, if not create a new one
    u_id = getUser(login_session)
    user = session.query(User).filter_by(id=u_id).one()
    login_user(user)

    return 'Login successful'


@users_blueprint.route('/ghconnect', methods=['GET'])
def ghconnect():
    # Check if state matches
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.args.get('code')

    # Exchanging client token for server-side token
    url = 'https://github.com/login/oauth/access_token'
    params = {'client_id': app.config['GH_CLIENT_ID'],
              'client_secret': app.config['GH_SECRET'],
              'code': access_token,
              'state': login_session['state']}
    headers = {'Accept': 'application/json'}
    data = requests.post(url, headers=headers, params=params)
    result = data.json()
    token = result['access_token']

    # Use token to get user info from API
    url = 'https://api.github.com/user'
    headers = {'Authorization': 'token %s' % token}
    data = requests.get(url, headers=headers)
    result = data.json()

    # Store data in session
    login_session['provider'] = 'github'
    if result['name'] is not None:
        login_session['username'] = result['name']
    else:
        login_session['username'] = result['login']
    if result['email'] is not None:
        login_session['email'] = result['email']
    else:
        login_session['email'] = '%s@%s.gh' % (result['id'], result['login'])
    login_session['github_id'] = result['id']
    login_session['credentials'] = token
    login_session['picture'] = result['avatar_url']

    # check if user exists, if not create a new one
    u_id = getUser(login_session)
    user = session.query(User).filter_by(id=u_id).one()
    login_user(user)

    return redirect(url_for('users.loginSuccess'))


@users_blueprint.route('/disconnect')
@login_required
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        if login_session['provider'] == 'facebook':
            fbdisconnect()
        if login_session['provider'] == 'github':
            ghdisconnect()
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        del login_session['credentials']
        flash('You have been logged out.', 'success')
        logout_user()
        return redirect(url_for('items.showHome'))
    else:
        flash('You were not logged in.', 'error')
        return redirect(url_for('items.showHome'))
