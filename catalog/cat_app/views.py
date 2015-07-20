from flask import render_template
from cat_app import app

@app.route('/')
def homepage():
	# from cat_app.models import Category, Product
	# products = Product.query.all()
	# categories = Category.query.all()
	return render_template('home.html')

@app.route('/catalog/create-product', methods = ['GET', 'POST'])
def new_product():
	return render_template('edit-product.html')