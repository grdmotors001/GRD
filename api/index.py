"""Vercel entry point for the existing Flask application."""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app

# Vercel's Python runtime discovers the Flask WSGI app named `app`.
