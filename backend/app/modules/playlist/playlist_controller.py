from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.modules.playlist.playlist_repository import PlaylistRepository
from app.modules.playlist.playlist_service import PlaylistService
from app.modules.playlist.playlist_schema import PlaylistUpdate, PlaylistResponse

from app.core.security.dependencies import get_current_user, require_role
from app.models.playlist import Playlist
from app.models.user import User  # se você tiver User model

router = APIRouter()


# 🔧 Service factory
def get_playlist_service(db: Session = Depends(get_db)):
    repo = PlaylistRepository(db)
    return PlaylistService(repo)


# 🎵 CREATE (mantive seu estilo direto no DB, mas ideal seria service)
@router.post("/spotify")
def criar_playlist(data: dict, db: Session = Depends(get_db)):
    playlist = Playlist(
        playlist=data["playlist"],
        nome=data["nome"],
        artista=data["artista"],
        album=data["album"],
        duracao=data["duracao"],
        cover=data["cover"],
        album_cover=data["album_cover"],
        track_url=data["track_url"]
    )

    db.add(playlist)
    db.commit()
    db.refresh(playlist)

    return {"msg": "salvo", "id": playlist.id}


# 🎵 LISTAR TODOS
@router.get("/spotify")
def listar_playlists(db: Session = Depends(get_db)):
    playlists = db.query(Playlist).all()

    return [
        {
            "id": p.id,
            "playlist": p.playlist,
            "nome": p.nome,
            "artista": p.artista,
            "album": p.album,
            "duracao": p.duracao,
            "cover": p.cover,
            "album_cover": p.album_cover,
            "track_url": p.track_url
        }
        for p in playlists
    ]


# 🎤 ARTIST PAGE (CORRIGIDO)
@router.get("/artist/{artist}", response_model=list[PlaylistResponse])
def get_artist(
    artist: str,
    service: PlaylistService = Depends(get_playlist_service)
):
    return service.get_artist_tracks(artist)


@router.get("/album/{album}", response_model=list[PlaylistResponse])
def get_album(
    album: str,
    service: PlaylistService = Depends(get_playlist_service)
):
    return service.get_album_tracks(album)

# 🎧 EMBED (CORRIGIDO)
@router.get("/embed")
def embed(
    track_url: str,
    service: PlaylistService = Depends(get_playlist_service)
):
    html = service.get_spotify_embed(track_url)
    return {"embed": html}


# 🔍 GET BY ID
@router.get("/{playlist_id}", response_model=PlaylistResponse)
def get_by_id(
    playlist_id: UUID,
    service: PlaylistService = Depends(get_playlist_service),
    current_user: User = Depends(require_role(["admin"]))
):
    return service.get_by_id(playlist_id)


# ✏️ UPDATE
@router.put("/{playlist_id}", response_model=PlaylistResponse)
def update(
    playlist_id: UUID,
    playlist: PlaylistUpdate,
    service: PlaylistService = Depends(get_playlist_service),
    current_user: User = Depends(get_current_user)
):
    return service.update(playlist_id, playlist, current_user)


# 🗑 DELETE
@router.delete("/{playlist_id}", response_model=PlaylistResponse)
def delete(
    playlist_id: UUID,
    service: PlaylistService = Depends(get_playlist_service),
    current_user: User = Depends(require_role(["admin"]))
):
    return service.delete(playlist_id)