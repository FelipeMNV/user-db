import datetime as dt
import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from .base import db


class Post(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[sa.DateTime] = mapped_column(sa.DateTime, default=dt.datetime.now())
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, user_id={self.user_id!r})"
