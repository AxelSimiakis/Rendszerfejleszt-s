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

            if "address" in request:
                request.pop("address")

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
        # Itt pedig pontosan 8 szokoz!
        payload = PayloadSchema()
        payload.exp = int((datetime.now() + timedelta(minutes=30)).timestamp())
        payload.user_id = user.id
        payload.roles = RoleSchema().dump(obj=user.roles, many=True)
        
        return jwt.encode({'alg': 'RS256'}, PayloadSchema().dump(payload), current_app.config['SECRET_KEY']).decode()

    @staticmethod
    def user_login(request):
        try:
            user = db.session.execute(select(User).filter_by(email=request["email"])).scalar_one_or_none()
            if not user or not check_password_hash(user.password_hash, request["password"]):
                return False, "Incorrect e-mail or password!"
            
            user_schema = UserResponseSchema().dump(user)
            
            user_schema["token"] = UserService.token_generate(user)
            
            return True, user_schema
            
        except Exception as ex:
            return False, "Incorrect Login data!"