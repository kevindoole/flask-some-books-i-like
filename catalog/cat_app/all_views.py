from flask import render_template, request, flash, redirect, url_for
from cat_app import app, db, login_session
from cat_app.models import Product, Category
from cat_app.form_requests.product import ProductForm




@app.route('/reset')
def reset_db():
    db.drop_all()
    db.create_all()
    return 'done'


@app.route('/')
def homepage():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('home.html', products=products, categories=categories)


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

        product.name = form.name.data
        product.description = form.description.data
        product.category = category
        db.session.commit()
        flash(message='Product updated', category='success')

        url = url_for(
            'product', category_slug=category.slug, product_slug=product.slug)
        return redirect(url)

    return render_template('edit-product.html', form=form)


@app.route('/catalog/<string:product_slug>/delete', methods=['GET', 'POST'])
def delete_product(product_slug):
    if 'username' not in login_session:
        flash('You are not authorized to access that page. Please log in.')
        return redirect('/login')
    product = Product.query.filter(Product.slug == product_slug).one()
    if request.method == 'POST':
        db.session.delete(product)
        db.session.commit()
        flash('Deleted &ldquo;%s&rdquo;' % product.name)
        return redirect('/')
    return render_template('delete.html', product=product)

@app.route('/catalog/<string:category_slug>/items')
def catalog_archive(category_slug):
    category = Category.query.filter(Category.slug == category_slug).one()
    products = category.products.all()
    return render_template('home.html', products=products)
