import os
os.environ["DEBUSSY"] = "1"

import unittest
import tempfile
from cat_app import app

class TestCatalog(unittest.TestCase):

	def setUp(self):
		self.test_db = 'storage/test_catalog.db'
		app.config['DATABASE'] = 'sqlite:///' + self.test_db
		app.config['TESTING'] = True
		self.app = app.test_client()

		from cat_app.database import init_db_tables
		init_db_tables()

	def tearDown(self):
		os.unlink(self.test_db)

	def test_models(self):
		from cat_app.models import Category, Product
		from cat_app.database import db_session

		cat = Category(name = 'TestCategory')
		cats = Category.query.all()
		db_session.add(cat)
		db_session.commit()
		cat = Category.query.filter(Category.name == 'TestCategory').one()
		assert cat.name == 'TestCategory'

		prod = Product(name = 'TestProduct', description = 'This is a product', category = cat)
		db_session.add(prod)
		db_session.commit()
		prod = Product.query.filter(Product.name == 'TestProduct').one()
		assert prod.name == 'TestProduct'
		assert prod.description == 'This is a product'
		assert prod.category == cat


if __name__ == '__main__':
    unittest.main()