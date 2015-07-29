from flask import render_template, request, flash, redirect, url_for
from cat_app import app, db, login_session
from cat_app.models import Product, Category
from cat_app.form_requests.product import ProductForm
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
import os

secrets_path = os.path.join('/vagrant/catalog/cat_app', 'client_secrets.json')
CLIENT_ID = json.loads(open(secrets_path, 'r').read())['web']['client_id']


def anti_forgery_state_token():
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for x in range(32))


@app.route('/login')
def login():
    state = anti_forgery_state_token()
    login_session['state'] = state
    return render_template('login.html', state=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    auth_code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets(secrets_path, scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(auth_code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' %
        access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            "Token's user ID doesn't match given user ID.", 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's"), 401)
        print "Token's client ID does not match app's"
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['access_token'] = access_token
    login_session['gplus_id'] = gplus_id
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    params = {'access_token': access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    # login_session['email'] = data['email']

    flash("you are now logged in as %s" % login_session['username'])

    return 'logged in'


@app.route('/logout')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user is not connected'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        # del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/')
def homepage():
    products = Product.query.all()
    return render_template('home.html', products=products)


@app.route('/catalog/<string:category_slug>/<string:product_slug>')
def product(category_slug, product_slug):
    prod = Product.query.filter(
        Product.slug == product_slug, Category.slug == category_slug).one()
    return render_template('product.html', product=prod)


@app.route('/catalog/create-product', methods=['GET', 'POST'])
def new_product():
    if 'username' not in login_session:
        flash('You are not authorized to access that page. Please log in.')
        return redirect('/login')

    form = ProductForm(request.form)
    if request.method == 'POST' and form.validate():
        category_name = form.category.data
        categories = Category.query.filter(
            Category.name == category_name).all()
        if not len(categories):
            category = Category(name=category_name)
        else:
            category = categories[0]

        prod = Product(name=form.name.data, description=form.description.data,
                       category=category)
        db.session.add(prod)
        db.session.commit()
        flash(message='Product created', category='success')

        url = url_for(
            'product', category_slug=category.slug, product_slug=prod.slug)
        return redirect(url)

    return render_template('edit-product.html', form=form)


@app.route('/catalog/<string:product_slug>/edit', methods=['GET', 'POST'])
def edit_product(product_slug):
    if 'username' not in login_session:
        flash('You are not authorized to access that page. Please log in.')
        return redirect('/login')
    product = Product.query.filter(Product.slug == product_slug).one()
    product.category_name = product.category.name
    form = ProductForm(request.form, product)
    if request.method == 'POST' and form.validate():
        category_name = form.category.data
        categories = Category.query.filter(
            Category.name == category_name).all()
        if not len(categories):
            category = Category(name=category_name)
        else:
            category = categories[0]

        prod = Product(name=form.name.data, description=form.description.data,
                       category=category)
        db.session.add(prod)
        db.session.commit()
        flash(message='Product created', category='success')

        url = url_for(
            'product', category_slug=category.slug, product_slug=prod.slug)
        return redirect(url)

    return render_template('edit-product.html', form=form)


@app.route('/catalog/<string:category_slug>/items')
def catalog_archive(category_slug):
    category = Category.query.filter(Category.slug == category_slug).one()
    products = category.products.all()
    return render_template('home.html', products=products)
