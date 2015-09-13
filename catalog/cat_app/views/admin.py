"""Responds to admin page requests."""
# pylint: disable=F0401
# pylint: disable=invalid-name
# pylint: disable=E1101

from flask import render_template, request, flash, redirect, url_for
from flask import Blueprint, session, abort
from functools import wraps
from cat_app import app, db, login_session, token
from cat_app.models import Product, Category
from cat_app.form_requests.product import ProductForm
from werkzeug import secure_filename
import os
from wand.image import Image

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

admin = Blueprint('admin', __name__)


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


def make_thumbnail_path(image_path):
    """Appends '-thumbnail' to the end of an image filename, before the
    file extension."""
    filename_pieces = os.path.splitext(image_path)
    thumbnail_path = '-thumbnail'.join(filename_pieces)
    return thumbnail_path

app.jinja_env.globals['thumbnail'] = make_thumbnail_path


def image_from_form(form, existing_image_url=None):
    """Saves an image uploaded in a form request and returns the
    resulting URL."""
    image_url = existing_image_url

    form_file = request.files[form.image.name]
    if form_file.filename and allowed_file(form_file.filename):
        filename = secure_filename(form_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form_file.save(file_path)
        generate_thumbnail(file_path)
        return "/media/" + filename

    return image_url


def generate_thumbnail(image_path):
    """Generates a 300px thumbnail if an image is too large."""
    thumbnail_path = make_thumbnail_path(image_path)
    img = Image(filename=image_path)
    img_clone = img.clone()

    # We want to make sure the thumbnail width maxes out at 300px.
    if img.size[0] > 300:
        img_clone.transform(resize='300x9999>')

    # If the height is still greater than 300px after resizing, crop the
    # bottom off, given the title of books is most often up top.
    if img.size[1] > 300:
        img_clone.crop(width=300, height=300, gravity='north')

    img_clone.save(filename=thumbnail_path)


def allowed_file(filename):
    """Checks if the filename's extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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


def product_from_form(form, product=None, product_query=None):
    category = Category.find_or_create(form.category.data)

    details = {'name': form.name.data,
            'subhead': form.subhead.data,
            'author': form.author.data,
            'year': form.year.data,
            'description': form.description.data}

    if product is None:
        details['category'] = category
        details['image_url'] = image_from_form(form)
        product = Product(details)
    else:
        details['image_url'] = image_from_form(form, product.image_url)
        product.category = category
        for key in details:
            setattr(product, key, details[key])

    db.session.add(product)
    db.session.commit()

    return product


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

    prod = product_from_form(form)

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

    product = product_from_form(
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
