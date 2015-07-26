import os
import unittest
from cat_app import app, db, basedir
from cat_app.models import Product, Category
import flask


class TestCatalog(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'storage/test_catalog.db')
        app.config['TESTING'] = True
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_empty_db(self):
        homepage = self.app.get('/')
        assert 'No products' in homepage.data
        assert 'No categories' in homepage.data

    def test_models(self):
        cat = Category(name='TestCategory')
        cats = Category.query.all()
        db.session.add(cat)
        db.session.commit()
        cat = Category.query.filter(Category.name == 'TestCategory').one()
        assert cat.name == 'TestCategory'

        prod = Product(
            name='TestProduct', description='This is a product', category=cat)
        db.session.add(prod)
        db.session.commit()
        prod = Product.query.filter(Product.name == 'TestProduct').one()
        assert prod.name == 'TestProduct'
        assert prod.description == 'This is a product'
        assert prod.category == cat

    def test_only_authorized_users_can_access_admin_pages(self):
        with self.app as c:
            new_product_page = c.get('/catalog/create-product',
                                     follow_redirects=True)
            assert flask.request.path == '/'
            assert 'You are not authorized' in new_product_page.data

    def test_it_can_save_products(self):
        new_product_form = self.app.get('/catalog/create-product')
        assert '<input id="name' in new_product_form.data
        assert '<textarea id="description' in new_product_form.data
        assert '<input id="category' in new_product_form.data

        new_product_page = None
        with self.app as c:
            new_product_page = c.post('/catalog/create-product', data=dict(
                name='a new product',
                description='description text',
                category='test category'
            ), follow_redirects=True)
            assert flask.request.path == '/catalog/test-category/a-new-product'

        assert 'Product created' in new_product_page.data
        assert 'a new product' in new_product_page.data
        assert 'description text' in new_product_page.data
        prod = Product.query.first()
        assert 'a new product' == prod.name
        assert 'description text' == prod.description
        homepage = self.app.get('/')
        assert 'No products' not in homepage.data
        assert 'a new product' in homepage.data
        assert 'description text' not in homepage.data

    def test_it_validates_form_requests(self):
        new_product_page = None
        with self.app as c:
            new_product_page = c.post('/catalog/create-product', data=dict(
                name='',
                description='',
                category=''
            ), follow_redirects=True)
            assert flask.request.path == '/catalog/create-product'

        assert 'Product created' not in new_product_page.data
        assert 'This field is required' in new_product_page.data


if __name__ == '__main__':
    unittest.main()
