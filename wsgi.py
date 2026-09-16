from backend.app import app

application = app

# Backwards compatibility for older hosting setups.
# This lets gunicorn or WSGI servers import the app as `wsgi:application`.
