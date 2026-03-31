from sqlalchemy import Column, String, Integer,DateTime
from app.core.database import Base
from datetime import datetime, timezone


class TokenBlacklist(Base):

    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True)
    jti = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))