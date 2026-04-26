from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from apiflask import HTTPTokenAuth
from flask import current_app
from authlib.jose import jwt
from datetime import datetime

auth = HTTPTokenAuth()

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)


@auth.verify_token
def verify_token(token):
    """Verify JWT token from Authorization header"""
    try:
        data = jwt.decode(
            token.encode('ascii'),
            current_app.config['SECRET_KEY'],
        )
        
        # Check if token has expired
        if data.get("exp") and data["exp"] < int(datetime.now().timestamp()):
            return None
        
        return data
    except Exception as e:
        print(f"Token verification failed: {e}")
        return None


