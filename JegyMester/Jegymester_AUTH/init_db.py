from app import create_app
from app.extensions import db
from app.models.role import Role
from sqlalchemy import select

app = create_app()

with app.app_context():
    db.create_all()
    for role_name in ["guest", "User", "Admin"]:
        existing = db.session.execute(select(Role).filter_by(name=role_name)).scalar_one_or_none()
        if not existing:
            db.session.add(Role(name=role_name))
    db.session.commit()
    print("Adatbazis letrehozva, alap szerepkorok keszen: guest, User, Admin")
