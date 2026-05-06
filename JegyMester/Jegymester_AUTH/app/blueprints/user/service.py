from app.extensions import db
from .schemas import UserResponseSchema, PayloadSchema, RoleSchema
from app.models.user import User
from app.models.role import Role
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from authlib.jose import jwt
from flask import current_app

class UserService:
    @staticmethod
    def user_registrate(request):
        try:
            if db.session.execute(select(User).filter_by(email=request["email"])).scalar_one_or_none():
                return False, "E-mail already exists!"

            request.pop("address", None)
            password_to_hash = request.pop("password")
            user = User(**request)
            user.password_hash = generate_password_hash(password_to_hash)

            default_role = db.session.execute(select(Role).filter_by(name="guest")).scalar_one_or_none()
            if default_role:
                user.roles.append(default_role)

            db.session.add(user)
            db.session.commit()

            return True, UserResponseSchema().dump(user)
        except Exception as ex:
            print(f"Error: {ex}")
            db.session.rollback()
            return False, "Incorrect User data!"

    @staticmethod
    def token_generate(user: User):
        payload = {
            "exp": int((datetime.now() + timedelta(minutes=30)).timestamp()),
            "user_id": user.id,
            "roles": RoleSchema().dump(obj=user.roles, many=True),
        }
        return jwt.encode({'alg': 'HS256'}, PayloadSchema().dump(payload), current_app.config['SECRET_KEY']).decode()

    @staticmethod
    def user_login(request):
        try:
            user = db.session.execute(select(User).filter_by(email=request["email"])).scalar_one_or_none()
            if not user or not check_password_hash(user.password_hash, request["password"]):
                return False, "Incorrect e-mail or password!"

            user_schema = UserResponseSchema().dump(user)
            user_schema["token"] = UserService.token_generate(user)
            return True, user_schema
        except Exception:
            return False, "Incorrect Login data!"

    @staticmethod
    def get_user_by_id(user_id):
        user = db.session.get(User, user_id)
        if not user:
            return False, "User not found"
        return True, UserResponseSchema().dump(user)

    @staticmethod
    def list_user_roles(user_id):
        user = db.session.get(User, user_id)
        if not user:
            return False, "User not found"
        return True, RoleSchema().dump(user.roles, many=True)

    @staticmethod
    def user_list_roles():
        roles = db.session.execute(select(Role)).scalars().all()
        return True, RoleSchema().dump(roles, many=True)
