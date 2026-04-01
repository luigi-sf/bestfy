from app.models.playlist import Playlist
from sqlalchemy.orm import Session
from uuid import UUID
from app.modules.playlist.playlist_schema import PlaylistCreate, PlaylistUpdate
from app.models.playlist import Playlist
from sqlalchemy import func



class PlaylistRepository:

    def __init__(self, db: Session):
        self.db = db

   
   # CREATE
    def create(self, playlist: PlaylistCreate):

        dbPlaylist = Playlist(
            **playlist.model_dump()
    )

        self.db.add(dbPlaylist)
        self.db.commit()
        self.db.refresh(dbPlaylist)

        return dbPlaylist
    
    
    
    #GET TRACK
    def get_by_track_url(self, track_url: str):
        return self.db.query(Playlist).filter(
        Playlist.track_url == track_url
    ).first()


    #LIST
    def list(self):
        return self.db.query(Playlist).all() #self.db.query e filtra oq vc vai pegar

    
    #GET ID
    def get_by_id(self, playlist_id: UUID):
        return self.db.query(Playlist).filter(Playlist.id == playlist_id).first()


    #UPDATE
    def update(self, playlist_id: UUID, data: PlaylistUpdate):

        dbPlaylist = self.get_by_id(playlist_id)

        if not dbPlaylist:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(dbPlaylist, key, value)

        self.db.commit()
        self.db.refresh(dbPlaylist)

        return dbPlaylist
    
    #GET ARTIST
    def get_by_artist(self, artist_name: str):
        return (
        self.db.query(Playlist)
        .filter(Playlist.artista.contains([artist_name]))
        .all()
    )
        
    
    #GET ALBUM   
    def get_by_album(self, album_name: str):
        return (
        self.db.query(Playlist)
        .filter(func.lower(Playlist.album).contains(album_name.lower()))
        .all()
    )

    # DELETE
    def delete(self, playlist_id: UUID):

        dbPlaylist = self.get_by_id(playlist_id)

        if not dbPlaylist:
            return None

        self.db.delete(dbPlaylist)
        self.db.commit()

        return dbPlaylist