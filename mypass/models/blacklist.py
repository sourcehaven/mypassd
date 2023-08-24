from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from mypass.models.base import Model


class TokenBlacklist(Model):
    __tablename__ = 'token_blacklist'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(sa.String(255))
    create_time: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())

    def __repr__(self):
        return str(self)

    def __str__(self):
        return (f'{self.__class__.__name__}('
                f'id={self.id}, '
                f'token={self.token}, '
                f'create_time={self.create_time})')
