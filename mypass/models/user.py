from typing import Optional
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
import sqlalchemy_utils as sau

from mypass import crypto
from .base import Model
from . import entry


class User(Model):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(sa.String(255), unique=True)
    firstname: Mapped[Optional[str]] = mapped_column(sa.Unicode(255))
    lastname: Mapped[Optional[str]] = mapped_column(sa.Unicode(255))
    email: Mapped[Optional[str]] = mapped_column(sau.EmailType(255))
    create_time: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())

    _password: Mapped[str] = mapped_column(sa.String(255), name='password')
    _token: Mapped[str] = mapped_column(sa.String(255), name='token')
    _salt: Mapped[str] = mapped_column(sa.String(255), name='salt')

    vault_entries: Mapped[list[entry.VaultEntry]] = relationship(cascade='all, delete-orphan')
    tags: Mapped[list[entry.Tag]] = relationship(cascade='all, delete-orphan')

    # noinspection PyShadowingBuiltins
    def __init__(
            self,
            id=None,
            *,
            username=None,
            password=None,
            secretpw=None,
            token=None,
            salt=None,
            firstname=None,
            lastname=None,
            email=None,
            stfu=False
    ):
        """
        Model class representing an application user.

        Parameters:
            id (int | None): primary key (not passed directly)
            username (str): the username
            password (str): master password which will be hashed
            token (str): one time given, secret token
            salt (str): salt used for password hashing and token encryption
            firstname (str | None): forename
            lastname (str | None): family name
            email (str | None): email address of the user
            stfu (bool): silence error messages explicitly
        """

        if not stfu:
            raise TypeError('You dont know what you are doing! Use create classmethod instead.')

        # noinspection PyTypeChecker
        self.id = id
        # noinspection PyTypeChecker
        self.username = username
        # noinspection PyTypeChecker
        self._password = password
        # noinspection PyTypeChecker
        self._token = token
        # noinspection PyTypeChecker
        self._salt = salt
        # noinspection PyTypeChecker
        self.firstname = firstname
        # noinspection PyTypeChecker
        self.lastname = lastname
        # noinspection PyTypeChecker
        self.email = email
        self._secretpw = secretpw

    @classmethod
    def create(cls, *, username=None, password=None, firstname=None, lastname=None, email=None):
        """
        Model class representing an application user.

        Parameters:
            username (str | None): the username
            password (str | None): master password which will be hashed
            firstname (str | None): forename
            lastname (str | None): family name
            email (str | None): email address of the user
        """

        salt = None
        secret_token = None
        hashed_pw = None
        if password is not None:
            salt = crypto.gen_salt()
            token = crypto.initpw(64)
            secret_token = crypto.encryptsecret(token, pw=password, salt=salt)
            hashed_pw = crypto.hashpw(password, salt)
        return cls(
            username=username, password=hashed_pw, secretpw=password, token=secret_token, salt=salt,
            firstname=firstname, lastname=lastname, email=email, stfu=True)

    def __repr__(self):
        return (f'{self.__class__.__name__}(id={self.id}, '
                f'username={self.username}, '
                f'firstname={self.firstname}, '
                f'lastname={self.lastname}, '
                f'email={self.email}, '
                f'password={self.password})')

    def unlock(self, pw):
        """
        Unlocks a queried object.

        Parameters:
            pw (str): the password for unlocking the object

        Returns:
            (User): the unlocked user object
        """

        return User(
            username=self.username, password=self._password, secretpw=pw, token=self._token,
            salt=self._salt, firstname=self.firstname, lastname=self.lastname, email=self.email, stfu=True)

    @property
    def token(self):
        if not hasattr(self, '_secretpw'):
            raise RuntimeError(f'{self.__class__.__name__} object at {id(self)} is not unlocked.')
        return crypto.decryptsecret(self._token, pw=self._secretpw, salt=self._salt)

    @property
    def password(self):
        if not hasattr(self, '_secretpw'):
            raise RuntimeError(f'{self.__class__.__name__} object at {id(self)} is not unlocked.')
        return self._secretpw

    @property
    def hashedpassword(self):
        return self._password

    @property
    def salt(self):
        return self._salt
