"""Creates the database needed for the catalog."""
# pylint: disable=F0401
# pylint: disable=invalid-name
# pylint: disable=E1101

from cat_app import db, images
from slugify import slugify
from datetime import datetime

def slug(context):
    """Makes a slug from a string, containing only letters,
    numbers and dashes."""
    if 'name' in context.current_parameters:
        return slugify(context.current_parameters['name'])

class Category(db.Model):
    """An sqlalchemy model of a product category."""

    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    slug = db.Column(db.String(250), default=slug, onupdate=slug)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    @staticmethod
    def by_name(name):
        """Get a list of categories by a name."""
        return Category.query.filter(Category.name == name).all()

    @staticmethod
    def by_slug(category_slug):
        """Gets a single category by it's slug."""
        return Category.query.filter(
            Category.slug == category_slug).first_or_404()

    @staticmethod
    def find_or_create(name):
        """Finds a matching bject from the DB, or generates a new one.
        Args: name (The category name)
        Returns: Instance of Category"""

        categories = Category.by_name(name)
        if categories:
            category = categories[0]
        else:
            category = Category(name=name)
            db.session.add(category)
            db.session.commit()

        return category


class Product(db.Model):
    """An sqlalchemy model of a product."""

    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    subhead = db.Column(db.String(250), nullable=True)
    author = db.Column(db.String(250))
    image_url = db.Column(db.String(250))
    year = db.Column(db.Integer)
    description = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow,
                        onupdate=datetime.utcnow)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=True)
    category = db.relationship('Category',
                               backref=db.backref('products', lazy='dynamic'))
    slug = db.Column(db.String(250), default=slug, onupdate=slug)

    def __init__(self, details):
        self.name = details['name']
        self.subhead = details['subhead']
        self.description = details['description']
        self.author = details['author']
        self.year = details['year']
        if 'image_url' in details and details['image_url'] is not None:
            image_url = details['image_url']
        else:
            image_url = "http://placehold.it/300x300"
        self.image_url = image_url

        if 'category' in details:
            self.category = details['category']

    @staticmethod
    def by_slug(product_slug):
        """Gets one product by slug."""
        return Product.query.filter(Product.slug == product_slug).first_or_404()

    @staticmethod
    def by_slug_and_cat(category_slug, product_slug):
        """Gets a single product from a category and product slug."""
        return Product.query.filter(
            Product.slug == product_slug,
            Category.slug == category_slug).first_or_404()

    @staticmethod
    def from_form(form, product=None):
        """Creates or updates a product from a wtf-form."""
        category = Category.find_or_create(form.category.data)

        details = {'name': form.name.data,
                   'subhead': form.subhead.data,
                   'author': form.author.data,
                   'year': form.year.data,
                   'description': form.description.data}

        if product is None:
            details['category'] = category
            details['image_url'] = images.image_from_form(form)
            product = Product(details)
        else:
            details['image_url'] = images.image_from_form(form, product.image_url)
            product.category = category
            for key in details:
                setattr(product, key, details[key])

        db.session.add(product)
        db.session.commit()

        return product
