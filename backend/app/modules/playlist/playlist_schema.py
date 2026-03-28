from pydantic import BaseModel
from typing import Optional

class PlaylistCreate(BaseModel):
    playlist:str
    nome: str
    artista: str
    album: str
    duracao: str
    cover:str
    album_cover:str


class PlaylistUpdate(BaseModel):
    nome: Optional[str] = None
    artista: Optional[str] = None
    album: Optional[str] = None
    duracao: Optional[str] = None
    cover: Optional[str] = None
    playlist: Optional[str] = None
    album_cover: Optional[str] = None
    


class PlaylistResponse(BaseModel):
    id: int
    playlist:str
    nome: str
    artista: str
    album: str
    duracao: str
    cover:str
    album_cover:str

    class Config:
        from_attributes = True