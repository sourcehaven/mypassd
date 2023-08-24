from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from mypass import crypto
from mypass.db import db
from .base import Model

VaultTag = Table(
    'vault_tag',
    db.metadata,
    Column('vault_id', ForeignKey('vault.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True),
)


class VaultEntry(Model):
    __tablename__ = 'vault'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id', ondelete='CASCADE'))
    username: Mapped[str] = mapped_column(sa.String(255))
    salt: Mapped[str] = mapped_column(sa.String(255), name='salt')
    title: Mapped[Optional[str]] = mapped_column(sa.String(255))
    website: Mapped[Optional[str]] = mapped_column(sa.String(255))
    notes: Mapped[Optional[str]] = mapped_column(sa.String(2048))
    folder: Mapped[Optional[str]] = mapped_column(sa.String(255))
    create_time: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)

    _parent_id: Mapped[Optional[int]] = mapped_column(sa.Integer, unique=True)
    _password: Mapped[str] = mapped_column(sa.String(255), name='password')

    tags: Mapped[list['Tag']] = relationship(
        secondary=VaultTag, back_populates='vault_entries', lazy='joined', innerjoin=True)

    # noinspection PyShadowingBuiltins
    def __init__(
            self,
            id=None,
            *,
            user_id=None,
            username=None,
            password=None,
            salt=None,
            title=None,
            website=None,
            notes=None,
            folder=None,
            stfu=False,
            _encryptionkey=None,
    ):
        """
        Model class representing a vault entry.

        Parameters:
            id (int | None):
            user_id (int | None):
            username (str | None):
            password (str | None):
            salt (str | None):
            title (str | None):
            website (str | None):
            notes (str | None):
            folder (str | None):
            stfu (bool):
            _encryptionkey (str | None):

        Raises:
            TypeError: if called without setting the stfu=True parameter
        """

        if not stfu:
            raise TypeError('You dont know what you are doing! Use create classmethod instead.')

        # noinspection PyTypeChecker
        self.id = id
        # noinspection PyTypeChecker
        self.user_id = user_id
        # noinspection PyTypeChecker
        self.username = username
        # noinspection PyTypeChecker
        self._password = password
        # noinspection PyTypeChecker
        self.salt = salt
        # noinspection PyTypeChecker
        self.title = title
        # noinspection PyTypeChecker
        self.website = website
        # noinspection PyTypeChecker
        self.notes = notes
        # noinspection PyTypeChecker
        self.folder = folder
        self._encryptionkey = _encryptionkey

    # noinspection PyShadowingBuiltins
    @classmethod
    def create(
            cls,
            id=None,
            *,
            user_id=None,
            username=None,
            password=None,
            title=None,
            website=None,
            notes=None,
            folder=None,
            encryptionkey=None,
    ):
        """
        Use this for the creation of a vault entry model.

        Parameters:
            id (int):
            user_id (int):
            username (str):
            password (str):
            title (str):
            website (str):
            notes (str):
            folder (str):
            encryptionkey (str):
        """

        if user_id is None or encryptionkey is None:
            from flask_jwt_extended import get_jwt_identity
            from mypass.api.com import IDENTITY_UID, IDENTITY_TOK
            identity = get_jwt_identity()
            if user_id is None:
                try:
                    user_id = identity[IDENTITY_UID]
                except RuntimeError:
                    pass
            if encryptionkey is None:
                try:
                    encryptionkey = identity[IDENTITY_TOK]
                except RuntimeError:
                    pass

        obj = cls(
            id=id, user_id=user_id, username=username, password=None, salt=None, title=title, website=website,
            notes=notes, folder=folder, _encryptionkey=encryptionkey, stfu=True)
        obj.salt = crypto.gen_salt()
        obj.password = password
        return obj

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (f'{self.__class__.__name__}(id={self.id}, '
                f'user_id={self.user_id}, '
                f'username={self.username}, '
                f'password={self.password}, '
                f'title={self.title}, '
                f'website={self.website})')

    @property
    def password(self):
        if not hasattr(self, '_encryptionkey') or self._encryptionkey is None:
            raise RuntimeError(
                f'{self.__class__.__name__} object at {id(self)} does not have an encryption key.\n'
                f'Set the object\'s password attribute')
        return crypto.decryptsecret(self._password, pw=self._encryptionkey, salt=self.salt)

    @password.setter
    def password(self, __value):
        """
        Parameters:
            __value (str): the value that will be salted and hashed to create a password
        """

        if not hasattr(self, '_encryptionkey') or self._encryptionkey is None:
            raise RuntimeError(f'{self.__class__.__name__} object at {id(self)} is not unlocked.')
        self._password: str = crypto.encryptsecret(__value, pw=self._encryptionkey, salt=self.salt)

    @property
    def encryptedpassword(self):
        return self._password

    @property
    def encryptionkey(self):
        if hasattr(self, '_encryptionkey'):
            return self._encryptionkey
        return None

    @encryptionkey.setter
    def encryptionkey(self, __value):
        """

        Parameters:
            __value (str): sets the secret key for password encryption (usually user token)
        """

        self._encryptionkey = __value

    @property
    def parent_id(self):
        return self._parent_id


class Tag(Model):
    __tablename__ = 'tag'
    __table_args__ = (
        UniqueConstraint('name', 'user_id'),
        {'extend_existing': True})

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id', ondelete='CASCADE'))

    name: Mapped[int] = mapped_column(sa.String(255))
    description: Mapped[Optional[str]] = mapped_column(sa.String(255))
    create_time: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())

    vault_entries: Mapped[list['VaultEntry']] = relationship(
        secondary=VaultTag, back_populates='tags', lazy='joined', innerjoin=True)

    def __repr__(self):
        return (f'{self.__class__.__name__}(id={self.id}, '
                f'user_id={self.user_id}'
                f'name={self.name}, '
                f'description={self.description}, '
                f'create_time={self.create_time})')
