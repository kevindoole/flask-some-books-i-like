"""Creates the database needed for the catalog."""
from cat_app import db
from slugify import slugify

def slug(context):
	slug = slugify(context.current_parameters['name'])
	return slug

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    slug = db.Column(db.String(250), default=slug, onupdate=slug)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    category = db.relationship(Category)
    slug = db.Column(db.String(250), default=slug, onupdate=slug)

    def __init__(self, name, description, category):
        self.name = name
        self.description = description
        self.category = category
