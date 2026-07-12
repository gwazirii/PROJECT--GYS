# wsgi.py — production entry point
# Gunicorn target:  gunicorn wsgi:application
from app import application  # noqa: F401
