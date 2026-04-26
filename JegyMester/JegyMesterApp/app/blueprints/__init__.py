from app.extensions import auth
from apiflask import HTTPError


def role_required(roles):
    """Decorator to check if user has required roles"""
    def wrapper(fn):
        def decorated_function(*args, **kwargs):
            user_roles = [item["name"] for item in auth.current_user.get("roles", [])]
            for role in roles:
                if role in user_roles:
                    return fn(*args, **kwargs)
            raise HTTPError(message="Access denied", status_code=403)
        return decorated_function
    return wrapper