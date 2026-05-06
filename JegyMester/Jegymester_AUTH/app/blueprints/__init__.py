from app.extensions import auth

from flask import current_app

from authlib.jose import jwt

from datetime import datetime

from apiflask import HTTPError

@auth.verify_token

def verify_token(token):

    try:

        data = jwt.decode(

            token.encode('ascii'),

          

            current_app.config['SECRET_KEY'],

        )

        if data["exp"] < int(datetime.now().timestamp()):

            return None

        return data

    except:

        return None

def role_required(roles):

    def wrapper(fn):

        def decorated_function(*args, **kwargs):

            user_roles = [item["name"] for item in auth.current_user.get("roles")]

            for role in roles:

                if role in user_roles:

                    return fn(*args, **kwargs)       

            raise HTTPError(message="Access denied", status_code=403)

        return decorated_function

    return wrapper