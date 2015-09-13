"""Responds to admin page requests."""
# pylint: disable=F0401
# pylint: disable=invalid-name
# pylint: disable=E1101

from flask import render_template, request, flash, redirect, url_for
from flask import Blueprint, session, abort
from functools import wraps
from cat_app import app, db, login_session, token, images
from cat_app.models import Product, Category
from cat_app.form_requests.product import ProductForm
import os

admin = Blueprint('admin', __name__)

app.jinja_env.globals['thumbnail'] = images.make_thumbnail_path

@admin.before_request
def csrf_protect():
    """Checks that the session token matches a token submitted with a form."""
    if not app.config['WTF_CSRF_ENABLED']:
        return

    if request.method == "POST":
        session_token = session.pop('_csrf_token', None)
        form_token = request.form.get('_csrf_token')
        if not session_token or session_token != form_token:
            abort(403)


def generate_csrf_token():
    """Generates a csrf token."""
    if '_csrf_token' not in session:
        session['_csrf_token'] = token()
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token


def login_required(f):
    """Decorates views to ensure they can only be accessed by
    logged in users."""
    @wraps(f)
    def protected_route(*args, **kwargs):
        """Redirects to a login page if the current user is not logged in."""
        if 'username' not in login_session:
            flash('You are not authorized to access that page. Please log in.')
            return redirect('/login')
        return f(*args, **kwargs)
    return protected_route


@admin.route('/catalog/create-product')
@login_required
def new_product():
    """Presents and processes new products."""
    form = ProductForm(request.form)
    return render_template('admin/edit-product.html', form=form)


@admin.route('/catalog/create-product', methods=['POST'])
@login_required
def store_product():
    form = ProductForm(request.form)

    if not form.validate():
        return render_template('admin/edit-product.html', form=form)

    prod = Product.from_form(form)

    flash(message='Product created', category='success')

    url = url_for('frontend.product',
                  category_slug=prod.category.slug,
                  product_slug=prod.slug)
    return redirect(url)


@admin.route('/catalog/<string:product_slug>/edit')
@login_required
def edit_product(product_slug):
    """Presents and processes the form to edit products."""
    product = Product.query.filter(Product.slug == product_slug).one()
    form = ProductForm(request.form, product)

    return render_template(
        'admin/edit-product.html', form=form, product=product)


@admin.route('/catalog/<string:product_slug>/edit', methods=['POST'])
@login_required
def update_product(product_slug):
    product_query = Product.query.filter(Product.slug == product_slug)
    product = product_query.one()
    form = ProductForm(request.form, product)

    if not form.validate():
        return render_template(
            'admin/edit-product.html', form=form, product=product)

    product = Product.from_form(
        form, product=product, product_query=product_query)

    flash(message='Product updated', category='success')

    url = url_for('frontend.product', category_slug=product.category.slug,
                  product_slug=product.slug)
    return redirect(url)


@admin.route('/catalog/<string:product_slug>/delete', methods=['GET', 'POST'])
@login_required
def delete_product(product_slug):
    """Deletes a product."""
    product = Product.query.filter(Product.slug == product_slug).one()
    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash('Deleted &ldquo;%s&rdquo;' % product.name)
        return redirect('/')
    return render_template('admin/delete.html', product=product)
