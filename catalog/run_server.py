"""Runs a local server."""
from cat_app import app

app.debug = True
app.run(host='0.0.0.0', port=8000)
