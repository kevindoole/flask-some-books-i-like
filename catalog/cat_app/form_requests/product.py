"""Form config and validation for products."""
# pylint: disable=F0401
# pylint: disable=invalid-name
# pylint: disable=E1101

from wtforms import Form, TextField, FileField, TextAreaField, validators


class ProductForm(Form):
    """Wtf-forms field definitions."""
    name = TextField(
        'name', [validators.Length(min=4, max=250), validators.required()])
    description = TextAreaField('description', [validators.required()])
    category = TextField(
        'category', [validators.Length(min=4, max=250), validators.required()])
    author = TextField(
        'author', [validators.Length(min=4, max=250), validators.required()])
    year = TextField(
        'year', [validators.Length(min=4, max=4), validators.required()])
    subhead = TextField(
        'subhead', [validators.Length(min=4, max=250), validators.required()])
    image = FileField('Image File')
