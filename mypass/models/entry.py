from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Model
from .user import User


class VaultEntry(Model):
    __tablename__ = 'vault'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey('user.id', ondelete='CASCADE'))
    user: Mapped[User] = relationship(lazy='joined', innerjoin=True)
    username: Mapped[str] = mapped_column(sa.String(255))
    password: Mapped[str] = mapped_column(sa.String(255))
    salt: Mapped[str] = mapped_column(sa.String(255))
    title: Mapped[Optional[str]] = mapped_column(sa.String(255))
    website: Mapped[Optional[str]] = mapped_column(sa.String(255))
    notes: Mapped[Optional[str]] = mapped_column(sa.String(2048))
    folder: Mapped[Optional[str]] = mapped_column(sa.String(255))

    def __init__(
            self,
            pk=None,
            *,
            uid=None,
            username=None,
            password=None,
            salt='',
            title=None,
            website=None,
            notes=None,
            folder=None
    ):
        self.id = pk
        self.user_id = uid
        self.username = username
        self.password = password
        self.salt = salt
        self.title = title
        self.website = website
        self.notes = notes
        self.folder = folder

    def __repr__(self) -> str:
        return (f'VaultEntry(id={self.id}, '
                f'user_id={self.user_id}, '
                f'username={self.username}, '
                f'password={self.password}, '
                f'title={self.title}, '
                f'website={self.website})')
