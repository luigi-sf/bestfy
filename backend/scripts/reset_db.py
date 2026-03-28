from app.core.database import Base, engine

from app.models.playlist import Playlist
from app.models.user import User
from app.models.blacklist import TokenBlacklist

print("Resetando banco...")

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Banco resetado!")