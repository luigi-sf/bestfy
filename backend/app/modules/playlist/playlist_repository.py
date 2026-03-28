from app.models.playlist import Playlist
from sqlalchemy.orm import Session
from uuid import UUID
from app.modules.playlist.playlist_schema import PlaylistCreate, PlaylistUpdate



class PlaylistRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, playlist: PlaylistCreate):

        dbPlaylist = Playlist(
            **Playlist.model_dump() # tranforma o model em dic ai ele passa sozinho
        )

        self.db.add(dbPlaylist)
        self.db.commit()
        self.db.refresh(dbPlaylist)

        return dbPlaylist

    def list(self):
        return self.db.query(Playlist).all() #self.db.query e filtra oq vc vai pegar

    def get_by_id(self, playlist_id: UUID):
        return self.db.query(Playlist).filter(Playlist.id == playlist_id).first()


    def update(self, playlist_id: UUID, user: PlaylistUpdate):

        dbPlaylist = self.get_by_id(playlist_id)

        if not dbPlaylist:
            return None

        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(dbPlaylist, key, value)

        self.db.commit()
        self.db.refresh(dbPlaylist)

        return dbPlaylist

    def delete(self, playlist_id: UUID):

        dbPlaylist = self.get_by_id(playlist_id)

        if not dbPlaylist:
            return None

        self.db.delete(dbPlaylist)
        self.db.commit()

        return dbPlaylist