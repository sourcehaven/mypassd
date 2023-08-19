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
    forename: Mapped[Optional[str]] = mapped_column(sa.Unicode(255))
    surename: Mapped[Optional[str]] = mapped_column(sa.Unicode(255))
    email: Mapped[Optional[str]] = mapped_column(sau.EmailType(255))
    _password: Mapped[str] = mapped_column(sa.String(255), name='password')
    _token: Mapped[str] = mapped_column(sa.String(255), name='token')
    _salt: Mapped[str] = mapped_column(sa.String(255), name='salt')

    def __init__(
            self,
            pk=None,
            *,
            username=None,
            password=None,
            secretpw=None,
            token=None,
            salt=None,
            forename=None,
            surename=None,
            email=None,
            stfu=False
    ):
        """
        Model class representing an application user.

        Parameters:
            pk (int | None): primary key (not passed directly)
            username (str): the username
            password (str): master password which will be hashed
            token (str): one time given, secret token
            salt (str): salt used for password hashing and token encryption
            forename (str | None): firstname
            surename (str | None): lastname
            email (str | None): email address of the user
            stfu (bool): silence error messages explicitly
        """

        if not stfu:
            raise TypeError('You dont know what you are doing! Use create classmethod instead.')

        # noinspection PyTypeChecker
        self.id = pk
        # noinspection PyTypeChecker
        self.username = username
        # noinspection PyTypeChecker
        self._password = password
        # noinspection PyTypeChecker
        self._token = token
        # noinspection PyTypeChecker
        self._salt = salt
        # noinspection PyTypeChecker
        self.forename = forename
        # noinspection PyTypeChecker
        self.surename = surename
        # noinspection PyTypeChecker
        self.email = email
        self._secretpw = secretpw

    @classmethod
    def create(cls, pk=None, *, username=None, password=None, forename=None, surename=None, email=None):
        """
        Model class representing an application user.

        Parameters:
            pk (int | None): primary key (not passed directly)
            username (str | None): the username
            password (str | None): master password which will be hashed
            forename (str | None): firstname
            surename (str | None): lastname
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
            pk=pk, username=username, password=hashed_pw, secretpw=password, token=secret_token, salt=salt,
            forename=forename, surename=surename, email=email, stfu=True)

    def __repr__(self):
        return (f'{self.__class__.__name__}(id={self.id}, '
                f'username={self.username}, '
                f'forename={self.forename}, '
                f'surename={self.surename}, '
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
            pk=self.id, username=self.username, password=self._password, secretpw=pw, token=self._token,
            salt=self._salt, forename=self.forename, surename=self.surename, email=self.email, stfu=True)

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
