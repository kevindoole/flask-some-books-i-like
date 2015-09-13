"""Handles image uploads."""
# pylint: disable=F0401
# pylint: disable=invalid-name
# pylint: disable=E1101

from cat_app import app
from flask import request
from werkzeug import secure_filename
import os
from wand.image import Image

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

def make_thumbnail_path(image_path):
    """Appends '-thumbnail' to the end of an image filename, before the
    file extension."""
    filename_pieces = os.path.splitext(image_path)
    thumbnail_path = '-thumbnail'.join(filename_pieces)
    return thumbnail_path


def image_from_form(form, existing_image_url=None):
    """Saves an image uploaded in a form request and returns the
    resulting URL."""
    image_url = existing_image_url

    form_file = request.files[form.image.name]
    if form_file.filename and allowed_file(form_file.filename):
        filename = secure_filename(form_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form_file.save(file_path)
        generate_thumbnail(file_path)
        return "/media/" + filename

    return image_url


def generate_thumbnail(image_path):
    """Generates a 300px thumbnail if an image is too large."""
    thumbnail_path = make_thumbnail_path(image_path)
    img = Image(filename=image_path)
    img_clone = img.clone()

    # We want to make sure the thumbnail width maxes out at 300px.
    if img.size[0] > 300:
        img_clone.transform(resize='300x9999>')

    # If the height is still greater than 300px after resizing, crop the
    # bottom off, given the title of books is most often up top.
    if img.size[1] > 300:
        img_clone.crop(width=300, height=300, gravity='north')

    img_clone.save(filename=thumbnail_path)


def allowed_file(filename):
    """Checks if the filename's extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS