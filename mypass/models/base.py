from sqlalchemy.orm import declarative_base

from mypass.db.db import db

Base = declarative_base()
Base.__abstract__ = True


class Model(db.Model):
    __abstract__ = True
