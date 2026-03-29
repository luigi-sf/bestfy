from fastapi import HTTPException
from app.modules.playlist.playlist_repository import PlaylistRepository
from app.modules.playlist.playlist_schema import PlaylistCreate, PlaylistUpdate
from uuid import UUID


class PlaylistService:

    def __init__(self, repo: PlaylistRepository):
        self.repo = repo

    # 🎵 CREATE
    def create(self, playlist: PlaylistCreate):

        return self.repo.create(playlist)

    # 📄 LIST
    def list(self):
        return self.repo.list()

    # 🔍 GET BY ID
    def get_by_id(self, playlist_id: UUID):

        playlist = self.repo.get_by_id(playlist_id)

        if not playlist:
            raise HTTPException(
                status_code=404,
                detail="Playlist nao encontrada"
            )

        return playlist

    # ✏️ UPDATE
    def update(self, playlist_id: UUID, data: PlaylistUpdate, current_user=None):

        db_playlist = self.repo.update(playlist_id, data)

        if not db_playlist:
            raise HTTPException(
                status_code=404,
                detail="Playlist not found"
            )

        return db_playlist

    # 🗑 DELETE
    def delete(self, playlist_id: UUID):

        playlist = self.repo.delete(playlist_id)

        if not playlist:
            raise HTTPException(
                status_code=404,
                detail="Playlist nao encontrada"
            )

        return playlist

    # 🎤 ARTIST TRACKS (CORRIGIDO)
    def get_artist_tracks(self, artist_name: str):

        return self.repo.get_by_artist(artist_name)


    def get_album_tracks(self, album_name: str):

        return self.repo.get_by_album(album_name)
    
    # 🎧 SPOTIFY EMBED
    @staticmethod
    def get_spotify_embed(track_url: str):

        try:
            track_id = track_url.split("/")[-1].split("?")[0]

            return f"""
            <iframe
                src="https://open.spotify.com/embed/track/{track_id}?autoplay=1"
                width="100%"
                height="80"
                frameborder="0"
                allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
            </iframe>
            """

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Erro ao gerar embed: {str(e)}"
            )