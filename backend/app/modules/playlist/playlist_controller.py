from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.modules.playlist.playlist_repository import PlaylistRepository
from app.modules.playlist.playlist_service import PlaylistService
from app.modules.playlist.playlist_schema import PlaylistUpdate, PlaylistResponse, PlaylistCreate

from app.core.security.dependencies import get_current_user, require_role
from app.models.playlist import Playlist
from app.models.user import User 

router = APIRouter()



def get_playlist_service(db: Session = Depends(get_db)):
    repo = PlaylistRepository(db)
    return PlaylistService(repo)


# CREATE
@router.post("/spotify", response_model=PlaylistResponse)
def criar_playlist(
    data: PlaylistCreate,
    service: PlaylistService = Depends(get_playlist_service)
):
    return service.create(data)


# LISTAR ALL
@router.get("/spotify", response_model=list[PlaylistResponse])
def listar_playlists(
    service: PlaylistService = Depends(get_playlist_service)
):
    return service.list()


#  ARTIST 
@router.get("/artist/{artist}", response_model=list[PlaylistResponse])
def get_artist(
    artist: str,
    service: PlaylistService = Depends(get_playlist_service)
):
    return service.get_artist_tracks(artist)


# ALBUM
@router.get("/album/{album}", response_model=list[PlaylistResponse])
def get_album(
    album: str,
    service: PlaylistService = Depends(get_playlist_service)
):
    return service.get_album_tracks(album)

# EMBED 
@router.get("/embed")
def embed(
    track_url: str,
    service: PlaylistService = Depends(get_playlist_service)
):
    html = service.get_spotify_embed(track_url)
    return {"embed": html}


# GET BY ID - ADMIN
@router.get("/{playlist_id}", response_model=PlaylistResponse)
def get_by_id(
    playlist_id: UUID,
    service: PlaylistService = Depends(get_playlist_service),
    current_user: User = Depends(require_role(["admin"]))
):
    return service.get_by_id(playlist_id)


# UPDATE
@router.put("/{playlist_id}", response_model=PlaylistResponse)
def update(
    playlist_id: UUID,
    playlist: PlaylistUpdate,
    service: PlaylistService = Depends(get_playlist_service),
    current_user: User = Depends(get_current_user)
):
    return service.update(playlist_id, playlist, current_user)


# DELETE - ADMIN
@router.delete("/{playlist_id}", response_model=PlaylistResponse)
def delete(
    playlist_id: UUID,
    service: PlaylistService = Depends(get_playlist_service),
    current_user: User = Depends(require_role(["admin"]))
):
    return service.delete(playlist_id)