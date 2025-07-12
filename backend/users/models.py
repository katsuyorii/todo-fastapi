from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime, date, timezone

from core.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'
    
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password: Mapped[str]

    username: Mapped[str] = mapped_column(String(255))
    date_of_birth: Mapped[date] = mapped_column(nullable=True)
    # avatar_url

    is_active: Mapped[bool] = mapped_column(default=False)
    is_mailing: Mapped[bool] = mapped_column(default=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))