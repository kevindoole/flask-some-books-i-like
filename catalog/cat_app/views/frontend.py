from flask import render_template, request, flash, redirect, url_for, Blueprint
from cat_app import app, db, login_session
from cat_app.models import Product, Category
from cat_app.form_requests.product import ProductForm

frontend = Blueprint('frontend', __name__)

@frontend.route('/reset')
def reset_db():
    db.drop_all()
    db.create_all()
    return 'done'


@frontend.route('/')
def homepage():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('frontend/home.html', products=products, categories=categories)


@frontend.route('/catalog/<string:category_slug>/<string:product_slug>')
def product(category_slug, product_slug):
    prod = Product.query.filter(
        Product.slug == product_slug, Category.slug == category_slug).one()
    return render_template('frontend/product.html', product=prod)


@frontend.route('/catalog/<string:category_slug>/items')
def catalog_archive(category_slug):
    category = Category.query.filter(Category.slug == category_slug).one()
    products = category.products.all()
    return render_template('frontend/home.html', products=products)
