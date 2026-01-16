"use client"

import { observer } from "mobx-react-lite"
import { useRouter } from "next/navigation"
import { useTrackStore } from "@/stores/store-provider"
import { TrackItem } from "./track-item"
import { Track } from "@/lib/types"

interface GeneratedTracksProps {
  playingTrackId: string | null
  isPlaying: boolean
  onTrackSelect: (track: Track) => void
}

export const GeneratedTracks = observer(function GeneratedTracks({
  playingTrackId,
  isPlaying,
  onTrackSelect,
}: GeneratedTracksProps) {
  const store = useTrackStore()
  const router = useRouter()

  const handleRowClick = (id: string, status: string) => {
    // if (status === "success") {
    //   router.push(`/track/${id}`)
    // }
  }

  const tracks = store.filteredTracks

  if (tracks.length === 0) {
    return (
      <div className="py-16 text-center">
        <p className="text-sm text-muted-foreground">No tracks yet. Generate your first one above.</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-medium text-foreground">Library</h2>
        <span className="text-xs text-muted-foreground">{tracks.length} tracks</span>
      </div>

      <div className="border border-border rounded-lg divide-y divide-border">
        {tracks.map((track) => (
          <TrackItem
            key={track.id}
            track={track}
            isPlaying={playingTrackId === track.id && isPlaying}
            onPlay={() => onTrackSelect(track)}
            onClick={() => {}}
            // onDelete={() => store.deleteTrack(track.id)}
            // onClick={() => handleRowClick(track.id, track.status)}
          />
        ))}
      </div>
    </div>
  )
})
