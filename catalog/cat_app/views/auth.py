"""Handles user authentication with oath2."""
# pylint: disable=F0401
# pylint: disable=invalid-name
# pylint: disable=E1101

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response, Blueprint, render_template, request
from flask import flash, redirect
import requests
import os
from cat_app import login_session, token

secrets_path = os.path.join('/vagrant/catalog/cat_app', 'client_secrets.json')
CLIENT_ID = json.loads(open(secrets_path, 'r').read())['web']['client_id']


auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    """Renders the login template."""
    state = token()
    login_session['state'] = state
    return render_template('auth/login.html', state=state)


def make_json_response(message, status):
    """Makes a json response with a given status code."""
    response = make_response(json.dumps(message), status)
    response.headers['Content-Type'] = 'application/json'
    return response

@auth.route('/gconnect', methods=['POST'])
def gconnect():
    """Handles Google+ login."""

    # Validate state token
    if request.args.get('state') != login_session['state']:
        return make_json_response('Invalid state parameter', 401)

    auth_code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(secrets_path, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(auth_code)
    except FlowExchangeError:
        return make_json_response(
            'Failed to upgrade the authorization code.', 401)

    # Check that the access token is valid
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        return make_json_response(result.get('error'), 500)

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        return make_json_response(
            "Token's user ID doesn't match given user ID.", 401)

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        return make_json_response(
            "Token's client ID does not match app's", 401)

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        return make_json_response('Current user is already connected', 200)

    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']

    flash("You are now logged in as %s" % login_session['username'], 'success')

    return 'logged in'


@auth.route('/logout')
def gdisconnect():
    """Handles Google+ disconnect (logs people out of this app)."""

    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user is not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    del login_session['access_token']
    del login_session['gplus_id']
    del login_session['username']
    del login_session['picture']

    if result['status'] == '200':
        flash('You logged out.', 'success')
    else:
        flash("""You logged out, but something went wrong revoking
              your Google+ token. It shouldn't matter at all,
              but if you have any concern, you can visit the
              authorized apps page of you google account to make
              sure this app has been revoked.""", 'success')

    return redirect('/')
