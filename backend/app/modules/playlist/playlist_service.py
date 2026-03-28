from fastapi import HTTPException
from app.modules.playlist.playlist_repository import PlaylistRepository
from app.modules.playlist.playlist_schema import PlaylistUpdate,PlaylistCreate,PlaylistResponse
from uuid import UUID


class PlaylistService:
    
    def __init__(self, repo:PlaylistRepository):
        self.repo = repo
        
    
    def create(self, playlist_id:UUID,playlist: PlaylistCreate):
        
        playlist_exist = self.repo.get_by_id(playlist_id)
        
        if playlist_exist:
            raise HTTPException(
                status_code=400,
                detail='Ja tem essa playlist'
            )
            
        return self.repo.create(playlist)
    
    
    def list (self):
        return self.repo.list()
    
    
    def get_by_id(self, playlist_id:UUID):
        
        playlist = self.repo.get_by_id(playlist_id)
        
        if not playlist:
            raise HTTPException(
                status_code=404,
                detail='playlist nao encontrada'
            )
            
        return playlist
    
    
    def update(self, playlist_id, data, current_user=None):

        db_playlist = self.repo.update(playlist_id, data)

        if not db_playlist:
            raise HTTPException(404, "Playlist not found")

        return db_playlist
    
    
    def delete (self,playlist_id:UUID):
        
        playlist = self.repo.delete(playlist_id)
        
        if not playlist:
            raise HTTPException(
                status_code=404,
                detail='playlist nao encontrada'
            )