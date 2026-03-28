from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.modules.playlist.playlist_repository import PlaylistRepository
from app.modules.playlist.playlist_service import PlaylistService
from app.modules.playlist.playlist_schema import PlaylistCreate, PlaylistUpdate, PlaylistResponse

from app.core.security.dependencies import get_current_user, require_role
from app.models.playlist import Playlist



router = APIRouter()

def get_playlist_service(db: Session = Depends(get_db)):
    repo = PlaylistRepository(db)
    return PlaylistService(repo)

        


@router.post("/spotify")
def criar_playlist(data: dict, db: Session = Depends(get_db)):
    playlist = Playlist(
        playlist=data["playlist"],
        nome=data["nome"],
        artista=data["artista"],
        album=data["album"],
        duracao=data["duracao"],
        cover= data['cover'],
        album_cover= data['album_cover']
    )

    db.add(playlist)
    db.commit()
    db.refresh(playlist)

    return {"msg": "salvo", "id": playlist.id}

@router.get("/spotify")
def listar_playlists(db: Session = Depends(get_db)):
    playlist = db.query(Playlist).all()
    # Retorna como lista de dicionários
    return [
        {"id": f.id,"playlist":f.playlist, "nome": f.nome, "artista": f.artista, "album": f.album, "duracao": f.duracao, "cover": f.cover, "album_cover": f.album_cover} 
        for f in playlist
    ]
    
@router.get("/{playlist_id}", response_model=PlaylistResponse)
def get_by_id(
    playlist_id: UUID,
    service: PlaylistService = Depends(get_playlist_service),
    current_user: Playlist = Depends(require_role(["admin"]))
):
    return service.get_by_id(playlist_id)


@router.put("/{playlist_id}", response_model=PlaylistResponse)
def update(
    playlist_id: UUID,
    playlist: PlaylistUpdate,
    service: PlaylistService = Depends(get_playlist_service),
    current_user: Playlist = Depends(get_current_user)
):
    return service.update(playlist_id, playlist, current_user)
    
    
    
    
    
    
    
@router.delete("/{playlist_id}", response_model=PlaylistResponse)
def delete(
    playlist_id: UUID,
    service: PlaylistService = Depends(get_playlist_service),
    current_user: Playlist = Depends(require_role(["admin"]))
):
    return service.delete(playlist_id)