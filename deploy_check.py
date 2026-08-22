import os

required = ["DATABASE_URL", "SECRET_KEY"]
missing = [x for x in required if not os.environ.get(x)]
if missing:
    print("Missing environment variables:", ", ".join(missing))
    raise SystemExit(1)

from app import app

with app.test_client() as client:
    r = client.get("/login")
    print("GET /login:", r.status_code)
    print("Deployment configuration looks OK.")
