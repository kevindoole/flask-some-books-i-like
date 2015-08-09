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
    subhead = db.Column(db.String(250), nullable=True)
    author = db.Column(db.String(250))
    year = db.Column(db.Integer)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=True)
    category = db.relationship('Category',
                               backref=db.backref('products', lazy='dynamic'))
    slug = db.Column(db.String(250), default=slug, onupdate=slug)

    def __init__(self, name, description, category, author, year, subhead=None):
        self.name = name
        self.subhead = subhead
        self.description = description
        self.category = category
        self.author = author
        self.year = year
