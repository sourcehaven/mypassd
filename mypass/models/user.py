from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
import sqlalchemy_utils as sau

from mypass import crypto
from .base import Model


class User(Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(255))
    password: Mapped[str] = mapped_column(sau.PasswordType(255, schemes=['pbkdf2_sha512']))
    token: Mapped[str] = mapped_column(sa.String(255))
    forename: Mapped[Optional[str]] = mapped_column(sa.Unicode(255))
    surename: Mapped[Optional[str]] = mapped_column(sa.Unicode(255))
    email: Mapped[Optional[str]] = mapped_column(sau.EmailType(255))
    salt: Mapped[str] = mapped_column(sa.String(255))

    def __init__(self, pk=None, *, username, password, forename=None, surename=None, email=None):
        """
        Model class representing an application user.

        Parameters:
            pk (int | None): primary key (not passed directly)
            username (str): the username
            password (str): master password which will be hashed
            forename (str | None): firstname
            surename (str | None): lastname
            email (str | None): email address of the user
        """

        self.id: int = pk
        self.username: str = username
        self.password: str = password
        self.password_ = password
        self.forename: str = forename
        self.surename: str = surename
        self.email: str = email
        self.token_ = crypto.initpw(nbytes=64)

    def __repr__(self) -> str:
        return (f'User(id={self.id}, '
                f'username={self.username}, '
                f'forename={self.forename}, '
                f'surename={self.surename}, '
                f'email={self.email}, '
                f'password={self.password})')

    def encrypt(self):
        """
        It is important that you call this method before saving your model to the database.
        This method is responsible for:
           - encrypting your master token
           - generating a salt
        """

        self.salt: str = crypto.gen_salt()
        self.token: str = crypto.encryptsecret(self.token_, pw=self.password_, salt=self.salt)

    def decrypt(self, pw):
        self.token_ = crypto.decryptsecret(self.token, pw=pw, salt=self.salt)
