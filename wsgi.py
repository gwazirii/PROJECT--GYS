# Root-level WSGI entry point for Render deployment
# This bridges to the actual Flask app in the backend directory
import sys
from pathlib import Path

# Make the backend directory importable for Gunicorn
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from app import application  # noqa: F401

# Export for gunicorn
__all__ = ["application"]
