from mypass.db.db import db


class Model(db.Model):
    __abstract__ = True
