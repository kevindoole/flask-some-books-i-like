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
    if request.method == "POST":
        token = session.pop('_csrf_token', None)
        if not token or token != request.form.get('_csrf_token'):
            abort(403)

def generate_csrf_token():
    if '_csrf_token' not in session:
        session['_csrf_token'] = token()
    return session['_csrf_token']

app.jinja_env.globals['csrf_token'] = generate_csrf_token


def make_thumbnail_path(image_path):
    filename = os.path.basename(image_path)
    filename_pieces = os.path.splitext(image_path)
    thumbnail_path = '-thumbnail'.join(filename_pieces)
    return thumbnail_path

app.jinja_env.globals['thumbnail'] = make_thumbnail_path

def generate_thumbnail(image_path):
    thumbnail_path = make_thumbnail_path(image_path)
    img = Image(filename=image_path)
    img_clone = img.clone()

    # We want to make sure the height is never > 300px for thumbnails.
    if img.size[1] > 300:
        img_clone.transform(resize='9999x300>')

    # If the width is still greater than 300px after resizing, crop
    # toward center.
    if img.size[0] > 300:
        img_clone.crop(width=300, height=300, gravity='center')

    img_clone.save(filename=thumbnail_path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        generate_thumbnail(file_path)
        return "/media/" + filename


def login_required(f):
    @wraps(f)
    def protected_route(*args, **kwargs):
        if 'username' not in login_session:
            flash('You are not authorized to access that page. Please log in.')
            return redirect('/login')
        return f(*args, **kwargs)
    return protected_route


@admin.route('/catalog/create-product', methods=['GET', 'POST'])
@login_required
def new_product():
    form = ProductForm(request.form)
    if request.method == 'POST' and form.validate():
        category_name = form.category.data
        categories = Category.query.filter(
            Category.name == category_name).all()
        if not len(categories):
            category = Category(name=category_name)
        else:
            category = categories[0]

        image_url = None
        file = request.files[form.image.name]
        if file.filename:
            image_url = upload_file(file)

        prod = Product(name=form.name.data, subhead=form.subhead.data,
                       author=form.author.data, image_url=image_url,
                       year=form.year.data, description=form.description.data,
                       category=category)
        db.session.add(prod)
        db.session.commit()
        flash(message='Product created', category='success')

        url = url_for('frontend.product', category_slug=category.slug,
                      product_slug=prod.slug)
        return redirect(url)

    return render_template('admin/edit-product.html', form=form)


@admin.route('/catalog/<string:product_slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_slug):
    product_query = Product.query.filter(Product.slug == product_slug)
    product = product_query.one()
    form = ProductForm(request.form, product)
    if request.method == 'POST' and form.validate():
        category_name = form.category.data
        categories = Category.query.filter(
            Category.name == category_name).all()
        if not len(categories):
            new_category = Category(name=category_name)
            db.session.add(new_category)
            db.session.commit()
            category = Category.query.order_by(Category.id.desc()).first()
        else:
            category = categories[0]

        image_url = product.image_url
        file = request.files[form.image.name]
        if file.filename:
            image_url = upload_file(file)

        product_query.update({"name": form.name.data,
            "description": form.description.data, "category_id": category.id,
            "image_url": image_url})
        db.session.commit()
        flash(message='Product updated', category='success')

        url = url_for('frontend.product', category_slug=category.slug,
                      product_slug=product.slug)
        return redirect(url)

    return render_template('admin/edit-product.html', form=form, product=product)


@admin.route('/catalog/<string:product_slug>/delete', methods=['GET', 'POST'])
@login_required
def delete_product(product_slug):
    product = Product.query.filter(Product.slug == product_slug).one()
    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash('Deleted &ldquo;%s&rdquo;' % product.name)
        return redirect('/')
    return render_template('admin/delete.html', product=product)
