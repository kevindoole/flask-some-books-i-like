import json
from flask import Flask, g, jsonify, Response, request, render_template, redirect, url_for

app = Flask(__name__)

app.config.update(dict(
    DATABASE = 'sqlite:///storage/catalog.db',
    DEBUG = True
))

@app.teardown_appcontext
def shutdown_session(exception=None):
	from database import db_session
	db_session.remove()