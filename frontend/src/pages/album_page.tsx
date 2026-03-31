import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import type { Playlist } from "../types/playlist/playlist"

export default function AlbumPage() {

  // PARAMS
  const { name } = useParams<{ name: string }>()

  // USESTATE
  const [tracks, setTracks] = useState<Playlist[]>([])
  const [currentEmbed, setCurrentEmbed] = useState<string | null>(null)

  useEffect(() => {
    if (!name) return

    fetch(`http://127.0.0.1:8000/album/${encodeURIComponent(name)}`)
      .then(res => res.json())
      .then(data => {
        if (!Array.isArray(data)) {
          console.error("Resposta inválida:", data)
          setTracks([])
          return
        }

        setTracks(data)
      })
      .catch(err => console.error(err))
  }, [name])

  // PLAYER
  async function openTrack(track_url: string) {
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/embed?track_url=${encodeURIComponent(track_url)}`
      )
      const data = await res.json()
      setCurrentEmbed(data.embed)
    } catch (err) {
      console.error("Erro ao carregar embed:", err)
    }
  }

  return (
    <div className="p-6 text-white bg-black min-h-screen pb-40">

      <h1 className="text-3xl font-bold mb-6">
        Álbum: {name}
      </h1>

      {/*TRACKS DO ÁLBUM */}
      <div className="grid gap-4">
        {tracks.map(track => (
          <div
            key={track.id}
            onClick={() => openTrack(track.track_url)}
            className="flex items-center gap-4 bg-zinc-800 p-4 rounded-lg cursor-pointer hover:bg-zinc-700 transition"
          >
            {/* COVER */}
            <img
              src={track.cover}
              alt={track.nome}
              className="w-16 h-16 rounded object-cover"
            />

            {/* INFO */}
            <div>
              <p className="font-bold">{track.nome}</p>
              <p className="text-sm text-zinc-400">{track.artista}</p>
            </div>
          </div>
        ))}
      </div>

      {/* PLAYER FIXO */}
      {currentEmbed && (
        <div className="fixed bottom-0 left-0 w-full bg-black border-t border-zinc-800 p-4 z-50">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm text-zinc-400">Tocando agora</span>

            <button
              onClick={() => setCurrentEmbed(null)}
              className="text-white text-sm"
            >
              Fechar
            </button>
          </div>

          <div dangerouslySetInnerHTML={{ __html: currentEmbed }} />
        </div>
      )}
    </div>
  )
}