from wtforms import Form, TextField, TextAreaField, validators

class ProductForm(Form):
	name = TextField('name', [validators.Length(min=4, max=250), validators.required()])
	description = TextAreaField('description', [validators.required()])
	category = TextField('category', [validators.Length(min=4, max=250), validators.required()])