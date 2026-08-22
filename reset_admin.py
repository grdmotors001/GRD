from app import app, db
from models import User

with app.app_context():
    u = User.query.filter_by(username="admin").first()
    if not u:
        u = User(username="admin")
        db.session.add(u)
    u.set_password("admin1")
    u.is_super_user = True
    u.permissions = "Y Y"
    db.session.commit()
    print("Password reset OK. Login with admin / admin1")