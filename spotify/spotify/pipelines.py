import requests

class SpotifyScraperPipeline:
    def process_item(self, item, spider):
        
        data = {
            "playlist": item.get("playlist"),
            "nome": item.get("nome"),
            "artista": item.get("artistas"),
            "album": item.get("album"),
            "duracao": item.get("duracao"),
            "cover": item.get('cover'),
            "album_cover": item.get('cover'),
            "track_url": item.get('track_url')
        }

        try:
            response = requests.post(
                "http://127.0.0.1:8000/spotify",
                json=data
            )

            print(f"Status: {response.status_code}")

        except Exception as e:
            print(f"Erro ao enviar: {e}")

        return item