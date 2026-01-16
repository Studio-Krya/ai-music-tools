"use client"

import { useState } from "react"
import { Header } from "@/components/header"
import { GenerationForm } from "@/components/generation-form"
import { CategoriesPanel } from "@/components/categories-panel"
import { GeneratedTracks } from "@/components/generated-tracks"
import { MainContent } from "@/components/main-content"
import { AudioPlayer } from "@/components/audio-player"
import { Track } from "@/lib/types"
import { useTrackStore } from "@/stores/store-provider"
import { observer } from "mobx-react-lite"

const HomePage = observer(function Home() {
  const store = useTrackStore()
  const [playingTrackId, setPlayingTrackId] = useState<string | null>(null)
  const [isPlaying, setIsPlaying] = useState(false)

  const playingTrack = playingTrackId ? store.getTrackById(playingTrackId) : null

  console.log(playingTrack)
  const handlePlayPause = () => {
    setIsPlaying(!isPlaying)
  }

  return (
    <div className="min-h-screen bg-background pb-24">
      <Header />

      <main className="max-w-6xl mx-auto px-6 py-12">
        <div className="grid grid-cols-12 gap-12">
          {/* Sidebar */}
          <aside className="col-span-3">
            <CategoriesPanel />
          </aside>

          {/* Main */}
          <div className="col-span-9 space-y-8">
            <GenerationForm />
            {/* <MainContent /> */}
            <GeneratedTracks
              playingTrackId={playingTrackId}
              isPlaying={isPlaying}
              onTrackSelect={(track) => {
                if (playingTrackId === track.id) {
                  setIsPlaying(!isPlaying)
                } else {
                  setPlayingTrackId(track.id)
                  setIsPlaying(true)
                }
              }}
            />
          </div>
        </div>
      </main>

      {/* Audio Player with built-in audio bar */}
      <AudioPlayer
        track={playingTrack || null}
        isPlaying={isPlaying}
        onPauseChanged={(paused) => {
          if (paused && isPlaying) {
            setIsPlaying(false)
          }
        }}
        onPlayPause={handlePlayPause}
      />
    </div>
  )
})

export default HomePage
