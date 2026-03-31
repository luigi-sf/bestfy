import { useRef, useState, useEffect } from "react"
import type { Playlist } from "../types/playlist/playlist"
import { ChevronLeft, ChevronRight } from "lucide-react"

type Props = {
  items: (Playlist & { onClick?: () => void })[]
  type?: "music" | "artist" | "album"
}

export function Carousel({ items, type }: Props) {
  const scrollRef = useRef<HTMLDivElement>(null)
  const [canScrollLeft, setCanScrollLeft] = useState(false)
  const [canScrollRight, setCanScrollRight] = useState(true)

  const checkScroll = () => {
    const el = scrollRef.current
    if (!el) return

    setCanScrollLeft(el.scrollLeft > 0)
    setCanScrollRight(el.scrollLeft < el.scrollWidth - el.clientWidth)
  }

  const scroll = (direction: "left" | "right") => {
    const el = scrollRef.current
    if (!el) return

    el.scrollBy({
      left: direction === "left" ? -300 : 300,
      behavior: "smooth",
    })
  }

  useEffect(() => {
    checkScroll()
  }, [items])

  return (
    <div className="relative group">
      {/* left seta*/}
      {canScrollLeft && (
        <button
          onClick={() => scroll("left")}
          className="absolute left-0 top-1/2 -translate-y-1/2 z-10 bg-black/70 p-2 rounded-full opacity-0 group-hover:opacity-100 transition"
        >
          <ChevronLeft size={20} />
        </button>
      )}

      {/* right seta */}
      {canScrollRight && (
        <button
          onClick={() => scroll("right")}
          className="absolute right-0 top-1/2 -translate-y-1/2 z-10 bg-black/70 p-2 rounded-full opacity-0 group-hover:opacity-100 transition"
        >
          <ChevronRight size={20} />
        </button>
      )}

      {/* LISTA */}
      <div
        ref={scrollRef}
        onScroll={checkScroll}
        className="flex gap-4 overflow-x-auto pb-4 scroll-smooth scrollbar-hide"
      >
        {items.map((item) => (
          <div
            key={item.id}
            onClick={item.onClick}
            className="min-w-[180px] bg-zinc-900 hover:bg-zinc-800 p-4 rounded-lg cursor-pointer"
          >
            <img
              src={
                type === "album"
                  ? item.album_cover || item.cover
                  : item.cover
              }
              className={`${type === "artist"
                  ? "w-[140px] h-[140px] rounded-full"
                  : "w-full h-[150px] rounded-md"
                } object-cover mb-4`}
            />

            <h3 className="text-sm font-semibold">
              {type === "artist"
                ? item.artista
                : type === "album"
                  ? item.album
                  : item.nome}
            </h3>

            <p className="text-xs text-gray-400">
              {type === "album"
                ? item.artista
                : type === "music"
                  ? item.artista
                  : "Artista"}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}