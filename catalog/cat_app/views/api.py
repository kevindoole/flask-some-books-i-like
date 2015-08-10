from flask import request, url_for
from flask import Blueprint, jsonify
from cat_app import app
from cat_app.models import Product, Category

api = Blueprint('api', __name__)


@api.route('/catalog.json')
def json_endpoint():
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
    response_data = {'Category': cat_data}
    return jsonify(response_data)
