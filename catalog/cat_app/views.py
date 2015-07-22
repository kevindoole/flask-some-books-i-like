from flask import render_template, request, flash, redirect, url_for
from cat_app import app, db
from cat_app.models import Product, Category
from cat_app.requests.product import ProductForm

@app.route('/')
def homepage():
	products = Product.query.all()
	return render_template('home.html', products=products)

@app.route('/catalog/<string:category_slug>/<string:product_slug>')
def product(category_slug, product_slug):
	prod = Product.query.filter(Product.slug == product_slug, Category.slug == category_slug).one()
	return render_template('product.html', product=prod)

@app.route('/catalog/create-product', methods = ['GET', 'POST'])
def new_product():
	form = ProductForm(request.form)
	if request.method == 'POST' and form.validate():
		category_name = form.category.data
		categories = Category.query.filter(Category.name == category_name).all()
		if not len(categories):
			category = Category(name=category_name)
		else:
			category = categories[0]

		prod = Product(name = form.name.data, description = form.description.data, category=category)
		db.session.add(prod)
		db.session.commit()
		flash(message='Product created', category='success')

		url = url_for('product', category_slug=category.slug, product_slug=prod.slug)
		return redirect(url)
		# return redirect(url)
	return render_template('edit-product.html', form=form)
