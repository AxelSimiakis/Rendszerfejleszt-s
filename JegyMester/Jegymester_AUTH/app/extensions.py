from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from apiflask import HTTPTokenAuth

auth = HTTPTokenAuth()

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class = Base)


