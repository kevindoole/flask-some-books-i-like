import os
from StringIO import StringIO
import unittest
from cat_app import app, db, basedir
from cat_app.models import Product, Category
import flask

def test_image():
    with open(os.path.join(basedir, 'assets/images/psychotic-reactions.jpg')) as test:
        imgStringIO = StringIO(test.read())
    return {'image': (imgStringIO, 'psychotic-reactions.jpg')}

class TestCatalog(unittest.TestCase):

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'storage/test_catalog.db')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False;
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def make_product(self):
        cat = Category(name='Gears')
        prod = Product({'name': 'Big Gears',
                        'description': 'blah',
                        'category': cat,
                        'subhead': 'this subhead',
                        'author': 'Kevin',
                        'year': 2014})
        db.session.add(prod)
        db.session.commit()

        return prod

    def test_empty_db(self):
        homepage = self.app.get('/')
        assert 'No products' in homepage.data
        assert 'No categories' in homepage.data

    def test_models(self):
        cat = Category(name='TestCategory')
        db.session.add(cat)
        db.session.commit()
        cat = Category.query.filter(Category.name == 'TestCategory').one()
        assert cat.name == 'TestCategory'

        prod = Product({'name': 'TestProduct',
                        'description': 'This is a product',
                        'category': cat,
                        'subhead': 'this subhead',
                        'author': 'Kevin',
                        'year': 2014})

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
            assert flask.request.path == '/login'
            assert 'You are not authorized' in new_product_page.data

    def test_it_can_save_products(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['username'] = 'testuser'

        new_product_form = self.app.get('/catalog/create-product')
        assert '<input id="name' in new_product_form.data
        assert '<textarea id="description' in new_product_form.data
        assert '<input id="category' in new_product_form.data

        new_product_page = None
        with self.app as c:
            new_product_page = c.post('/catalog/create-product', data=dict(
                test_image(),
                name='a new product',
                description='description text',
                category='test category',
                year='2014',
                author='Kevin',
                subhead='the subhead'
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
        with self.app as c:
            with c.session_transaction() as sess:
                sess['username'] = 'testuser'
        new_product_page = None
        with self.app as c:
            new_product_page = c.post('/catalog/create-product', data=dict(
                test_image(),
                name='',
                description='',
                category='',
                year=2014,
                author='Kevin',
                subhead='the subhead'
            ), follow_redirects=True)
            assert flask.request.path == '/catalog/create-product'

        assert 'Product created' not in new_product_page.data
        assert 'This field is required' in new_product_page.data

    def test_it_shows_correct_products_on_catalog_pages(self):
        cat1 = Category(name='Gears')
        cat2 = Category(name='Sprockets')
        db.session.add(cat1)
        db.session.add(cat2)
        db.session.commit()

        gears = Category.query.filter(Category.name == 'Gears').one()
        sprockets = Category.query.filter(Category.name == 'Sprockets').one()

        prod1 = Product({'name': 'Big Gears',
                        'description': 'blah',
                        'category': gears,
                        'subhead': 'this subhead',
                        'author': 'Kevin',
                        'year': 2014})
        prod2 = Product({'name': 'Small Sprockets',
                        'description': 'blah',
                        'category': sprockets,
                        'subhead': 'this subhead',
                        'author': 'Kevin',
                        'year': 2014})
        db.session.add(prod1)
        db.session.add(prod2)
        db.session.commit()

        gears_page = self.app.get('/catalog/gears/items')
        assert 'Small Sprockets' not in gears_page.data
        assert 'Big Gears' in gears_page.data

        sprockets_page = self.app.get('/catalog/sprockets/items')
        assert 'Small Sprockets' in sprockets_page.data
        assert 'Big Gears' not in sprockets_page.data

    def test_it_confirms_deletion(self):
        prod = self.make_product()

        with self.app as c:
            with c.session_transaction() as sess:
                sess['username'] = 'testuser'

        delete_page = self.app.get('/catalog/big-gears/delete')
        assert 'Are you sure? Delete &ldquo;Big Gears&rdquo;?' in delete_page.data

    def test_it_deletes_products(self):
        prod = self.make_product()

        with self.app as c:
            with c.session_transaction() as sess:
                sess['username'] = 'testuser'
            deleted_page = c.post('/catalog/big-gears/delete',
                follow_redirects=True)
            assert flask.request.path == '/'
            assert 'Deleted &ldquo;Big Gears&rdquo;' in deleted_page.data

    def test_it_can_edit_products(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['username'] = 'testuser'

        prod = self.make_product()

        edit_page = self.app.get('/catalog/big-gears/edit')
        assert 'value="Big Gears"' in edit_page.data
        assert 'value="Gears"' in edit_page.data
        assert '>blah<' in edit_page.data

        with self.app as c:
            edit_result = c.post('/catalog/big-gears/edit', data=dict(
                test_image(),
                name='Updated Big Gears',
                description='blah blah blah',
                category='Gromp',
                year='2014',
                author='Kevin',
                subhead='the subhead'
            ), follow_redirects=True)
            assert flask.request.path == '/catalog/gromp/updated-big-gears'
            assert 'Product updated' in edit_result.data
            assert 'Updated Big Gears' in edit_result.data
            assert 'blah blah blah' in edit_result.data
            assert 'Gromp' in edit_result.data

    def test_it_can_handle_file_uploads(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['username'] = 'testuser'

        create_result = c.post('/catalog/create-product', data=dict(
            test_image(),
            name='Updated Big Gears',
            description='blah blah blah',
            category='Gromp',
            year='2014',
            author='Kevin',
            subhead='the subhead'
        ), follow_redirects=True)
        assert 'src="/media/psychotic-reactions.jpg"' in create_result.data

    def test_it_provides_a_json_endpoint(self):
        prod = self.make_product()

        json = self.app.get('/catalog.json');
        assert '"name": "Gears"' in json.data
        assert '"author": "Kevin",' in json.data
        assert '"description": "blah",' in json.data
        assert '"image_url": "http://placehold.it/300x300",' in json.data
        assert '"name": "Big Gears",' in json.data
        assert '"subhead": "this subhead",' in json.data
        assert '"year": 2014' in json.data

if __name__ == '__main__':
    unittest.main()
