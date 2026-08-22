"""Initialize the configured database (Supabase PostgreSQL in production)."""
from app import app, _seed_defaults

with app.app_context():
    _seed_defaults()
    print("Database schema and default records are ready.")
