import scrapy

class PlaylistSpider(scrapy.Spider):
    name = "playlist"

    def start_requests(self):
        urls = [
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evO2VxlyE", # radio
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evNZYGncI", # slip
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evO34PI4g", # system
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evO47cwRq", # linkin
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evO2iBPiw", # beatles
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evO3WNHaM", # deaftones
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evO4BaAkp", # monkeys
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evO2n9pny", # elvis
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evO03DwPK", # mars
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evO4gTUOY", # eminem
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evO0LuyqI",#charlie brow
            "https://open.spotify.com/playlist/37i9dQZF1DXc2aPBXGmXrt",#justin bieber
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evO3nODok",#ze vaqueiro
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evO3P7qsU"#legiao urbana
            "https://open.spotify.com/playlist/37i9dQZF1DZ06evO1SVXaM"#michael jackeson
            
        ]

        for url in urls:
            yield scrapy.Request(
                url=url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                }
            )

    async def parse(self, response):
        page = response.meta["playwright_page"] # controle do navegador

        await page.wait_for_selector('div[data-testid="tracklist-row"]') # espera aparecer

        vistos = {}
        ultimo_total = 0

        for _ in range(50):  # limite máximo de tentativas
            content = await page.content()
            new_response = response.replace(body=content) # pega html atualizado
            playlist_nome = new_response.css(
            'h1[data-encore-id="text"].encore-text-headline-large::text').get()

            rows = new_response.css('div[data-testid="tracklist-row"]') # pega todas as divs de música
            
            for row in rows:
                
                nome = row.css('a[data-testid="internal-track-link"] div[dir="auto"]::text').get()
                
                artistas = list(dict.fromkeys([
                 a.strip() for a in row.css('a[href*="/artist/"]::text').getall() if a.strip()
                ]))
                
                album = row.css('a[href*="/album/"]::text').get()
                
                
                cover = row.css('img::attr(src)').get()
                
                #qualidade da imagem
                if cover:
                 cover = cover.replace("ab67616d00004851", "ab67616d0000b273")
                 
                tempos = row.css('div[data-encore-id="text"]::text').getall()

                duracao = None
                for t in tempos:
                    if ":" in t:
                        duracao = t
                        break

                if nome and nome not in vistos:
                    vistos[nome] = {
                        "playlist": playlist_nome,
                        "nome": nome,
                        "artistas": artistas,
                        "album": album,
                        "duracao": duracao,
                        "cover": cover,
                        "album_cover": cover
                    }

            if len(vistos) == ultimo_total:
                print("Parando: não encontrou novas músicas")
                break

            ultimo_total = len(vistos)

            # scroll controlado
            await page.mouse.wheel(0, 2500)
            await page.wait_for_timeout(800)

        await page.close()

        for item in vistos.values():
            yield item