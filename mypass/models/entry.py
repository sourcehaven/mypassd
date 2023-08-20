from datetime import datetime
from typing import Optional

import sqlalchemy as sa
from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Model
from ..db import db


VaultTag = Table(
    "vault_tag",
    db.metadata,
    Column("vault_id", ForeignKey("vault.id", ondelete='CASCADE'), primary_key=True),
    Column("tag_id", ForeignKey("tag.id", ondelete='CASCADE'), primary_key=True),
)


class VaultEntry(Model):
    __tablename__ = 'vault'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id', ondelete='CASCADE'))
    username: Mapped[str] = mapped_column(sa.String(255))
    password: Mapped[str] = mapped_column(sa.String(255))
    salt: Mapped[str] = mapped_column(sa.String(255))
    title: Mapped[Optional[str]] = mapped_column(sa.String(255))
    website: Mapped[Optional[str]] = mapped_column(sa.String(255))
    notes: Mapped[Optional[str]] = mapped_column(sa.String(2048))
    folder: Mapped[Optional[str]] = mapped_column(sa.String(255))
    create_time: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)

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
            folder=None
    ):
        self.id = id
        self.user_id = user_id
        self.username = username
        self.password = password
        self.salt = salt
        self.title = title
        self.website = website
        self.notes = notes
        self.folder = folder

    def __repr__(self):
        return (f'{self.__class__.__name__}(id={self.id}, '
                f'user_id={self.user_id}, '
                f'username={self.username}, '
                f'password={self.password}, '
                f'title={self.title}, '
                f'website={self.website})')


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
