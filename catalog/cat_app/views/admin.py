from flask import render_template, request, flash, redirect, url_for, Blueprint
from cat_app import app, db, login_session
from cat_app.models import Product, Category
from cat_app.form_requests.product import ProductForm

admin = Blueprint('admin', __name__)

@admin.route('/catalog/create-product', methods=['GET', 'POST'])
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
            'frontend.product', category_slug=category.slug, product_slug=prod.slug)
        return redirect(url)

    return render_template('admin/edit-product.html', form=form)


@admin.route('/catalog/<string:product_slug>/edit', methods=['GET', 'POST'])
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
            'frontend.product', category_slug=category.slug, product_slug=product.slug)
        return redirect(url)

    return render_template('admin/edit-product.html', form=form)


@admin.route('/catalog/<string:product_slug>/delete', methods=['GET', 'POST'])
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
    return render_template('admin/delete.html', product=product)