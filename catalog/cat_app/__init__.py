import json
from flask import Flask, g, jsonify, Response, request, render_template, redirect, url_for

app = Flask(__name__)

app.config.update(dict(
    DATABASE = 'sqlite:///storage/catalog.db',
    DEBUG = True
))

@app.route('/')
def homepage():
	# from models import Product, Category
	# products = Product.query.all()
	# categories = Category.query.all()
	return render_template('home.html')

@app.route('/catalog/create-product')
def new_product():
	return render_template('edit-product.html')

@app.teardown_appcontext
def shutdown_session(exception=None):
	from database import db_session
	db_session.remove()

if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 8000)