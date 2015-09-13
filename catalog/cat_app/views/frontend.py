"""Provides front end views."""
# pylint: disable=F0401
# pylint: disable=invalid-name
# pylint: disable=E1101

from flask import render_template
from flask import Blueprint, send_from_directory
from cat_app import app
from cat_app.models import Product, Category

frontend = Blueprint('frontend', __name__)


@app.route('/media/<filename>')
def uploaded_file(filename):
    """Displays an image file."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@frontend.route('/')
def homepage():
    """Shows the homepage."""
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('frontend/home.html', products=products,
                           categories=categories)


@frontend.route('/catalog/<string:category_slug>/<string:product_slug>')
def product(category_slug, product_slug):
    """Shows a single product."""
    prod = Product.by_slug_and_cat(category_slug, product_slug)
    return render_template('frontend/product.html', product=prod)


@frontend.route('/catalog/<string:category_slug>/items')
def catalog_archive(category_slug):
    """Shows a list of products attached to a category."""
    category = Category.by_slug(category_slug)
    products = category.products.all()
    categories = Category.query.all()
    return render_template('frontend/home.html',
                           products=products,
                           categories=categories,
                           selected_cat=category.name)
