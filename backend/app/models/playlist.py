from sqlalchemy import Column, String
from app.core.database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ARRAY
class Playlist(Base):
    __tablename__ = "playlist"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String, nullable=False)
    playlist = Column(String, nullable=False)
    artista = Column(ARRAY(String))
    album = Column(String, nullable=True)
    duracao = Column(String, nullable=True)
    cover = Column(String, nullable=True)
    album_cover = Column(String, nullable=True)
    track_url = Column(String, nullable=True)