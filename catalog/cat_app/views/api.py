from flask import request, url_for, Blueprint, jsonify
from cat_app import app
from cat_app.models import Product, Category
from werkzeug.contrib.atom import AtomFeed
from urlparse import urljoin


api = Blueprint('api', __name__)

def make_external(url):
	return urljoin(request.url_root, url)

def compile_feed_data():
    cat_data = []
    categories = Category.query.all()
    for c in categories:
        items = []
        for i in c.products.all():
            items.append({'id': i.id, 'name': i.name, 'author': i.author,
                          'subhead': i.subhead, 'year': i.year,
                          'description': i.description,
                          'image_url': i.image_url})
        cat_data.append({'id': c.id, 'name': c.name, 'items': items})
    return cat_data

@api.route('/catalog.atom')
def atom_endpoint():
    cat_data = compile_feed_data()
    feed = AtomFeed(
        'All books', feed_url=request.url, url=request.url_root)
    for i in Product.query.all():
        link = make_external(url_for('frontend.product',
            category_slug=i.category.slug,product_slug=i.slug))
        feed.add(i.name, i.description, content_type='html',
                 author=i.author, updated=i.updated, published=i.created,
                 url=link, categories=[{"term": i.category.name}])
    return feed.get_response()


@api.route('/catalog.json')
def json_endpoint():
    cat_data = compile_feed_data()
    response_data = {'Category': cat_data}
    return jsonify(response_data)
