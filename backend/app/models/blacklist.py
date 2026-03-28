from sqlalchemy import Column, String, Integer
from app.core.database import Base


class TokenBlacklist(Base):

    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True)