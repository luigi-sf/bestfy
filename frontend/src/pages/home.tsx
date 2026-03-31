import { useEffect, useState, useMemo } from "react"
import { useNavigate } from "react-router-dom"
import { Carousel } from "../components/carrosel"
import type { Playlist } from "../types/playlist/playlist"

export default function Home() {
  const [playlists, setPlaylists] = useState<Playlist[]>([])
  const [user, setUser] = useState<{ name: string } | null>(null)
  const [currentEmbed, setCurrentEmbed] = useState<string | null>(null)

  const navigate = useNavigate()

  function getGreeting() {
    const hour = new Date().getHours()

    if (hour >= 5 && hour < 12) return "Bom dia ☀️"
    if (hour >= 12 && hour < 18) return "Boa tarde 🌤️"
    if (hour >= 18 && hour < 23) return "Boa noite 🌙"
    return "Boa madrugada 🌙"
  }

  function shuffleArray<T>(array: T[]): T[] {
    return [...array].sort(() => Math.random() - 0.5)
  }

  function uniqueBy<T>(array: T[], key: keyof T): T[] {
    const seen = new Set()
    return array.filter((item) => {
      const value = item[key]
      if (seen.has(value)) return false
      seen.add(value)
      return true
    })
  }

  //USER
  useEffect(() => {
    const token = localStorage.getItem("token")

    fetch("http://127.0.0.1:8000/users/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(res => res.json())
      .then(data => setUser(data))
      .catch(() => setUser({ name: "Usuário" }))
  }, [])

  //PLAYLISTS
  useEffect(() => {
    fetch("http://127.0.0.1:8000/spotify")
      .then(res => res.json())
      .then(data => setPlaylists(data))
      .catch(err => console.error(err))
  }, [])

  //EMBED
  async function openTrack(track_url: string) {
    try {
      const res = await fetch(
        `http://127.0.0.1:8000/embed?track_url=${track_url}`
      )
      const data = await res.json()
      setCurrentEmbed(data.embed)
    } catch (err) {
      console.error("Erro ao carregar embed:", err)
    }
  }

  const shuffled = useMemo(() => shuffleArray(playlists), [playlists])

  const artistasUnicos = useMemo(
    () =>
      uniqueBy(
        shuffled.map(item => ({
          ...item,
          artista: Array.isArray(item.artista)
            ? item.artista[0]
            : item.artista?.split(",")[0]
        })),
        "artista"
      ),
    [shuffled]
  )

  const albunsUnicos = useMemo(
    () => uniqueBy(shuffled, "album"),
    [shuffled]
  )

  const musicas = shuffled.slice(0, 6)
  const artistas = artistasUnicos.slice(0, 10)
  const albuns = albunsUnicos.slice(0, 10)

  return (
    <div className="bg-black text-white min-h-screen p-6 pb-40">

      {/* HEADER */}
      <h1 className="text-3xl font-bold mb-6">
        {getGreeting()}, {user?.name || "Estranho"}
      </h1>

      {/*MÚSICAS */}
      <h2 className="text-2xl font-bold mb-4">Músicas em alta</h2>

      <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mb-10">
        {musicas.map((item) => (
          <div
            key={item.id}
            onClick={() => openTrack(item.track_url)}
            className="flex items-center bg-zinc-800 rounded-lg overflow-hidden hover:bg-zinc-700 transition cursor-pointer"
          >
            <img src={item.cover} className="w-16 h-16 object-cover" />
            <span className="ml-4 font-semibold">{item.nome}</span>
          </div>
        ))}
      </div>

      {/*ARTISTAS */}
      {artistas.length > 0 && (
        <>
          <h2 className="text-2xl font-bold mt-10 mb-4">
            Artistas populares
          </h2>

          <Carousel
            items={artistas.map(a => ({
              ...a,
              onClick: () =>
                navigate(`/artist/${encodeURIComponent(a.artista)}`)
            }))}
            type="artist"
          />
        </>
      )}

      {/* ÁLBUNS */}
      {albuns.length > 0 && (
        <>
          <h2 className="text-2xl font-bold mt-10 mb-4">
            Singles e álbuns que todo mundo gosta
          </h2>
          <Carousel items={albuns.map(a => ({
            ...a,
            onClick: () =>
              navigate(`/album/${encodeURIComponent(a.album)}`)
          }))}
            type="album" />
        </>
      )}

      {/*PLAYER FIXO */}
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