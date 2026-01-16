"use client"

import { useEffect, useRef, useState } from "react"
import { Track } from "@/lib/types"
import { Button } from "./ui/button"
import { Play, Pause, SkipBack, SkipForward } from "lucide-react"

interface AudioPlayerProps {
  track: Track | null
  onPauseChanged: (isPaused: boolean) => void
  isPlaying: boolean
  onPlayPause?: () => void
  onNext?: () => void
  onPrevious?: () => void
}

function formatTime(seconds: number): string {
  if (isNaN(seconds) || !isFinite(seconds)) return "0:00"
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, "0")}`
}

export function AudioPlayer({ 
  track, 
  onPauseChanged, 
  isPlaying,
  onPlayPause,
  onNext,
  onPrevious
}: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null)
  const previousSrcRef = useRef<string | null | undefined>(null)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const animationFrameRef = useRef<number | null>(null)

  const src = track?.audio_url

  // Handle URL changes - reload if different
  useEffect(() => {
    if (!audioRef.current) return

    const audio = audioRef.current

    // If src is null/undefined, pause and clear
    if (!src) {
      audio.pause()
      audio.src = ""
      previousSrcRef.current = null
      return
    }

    // If URL is different, reload
    if (src !== previousSrcRef.current) {
      audio.pause()
      audio.src = src
      audio.load() // Force reload
      previousSrcRef.current = src

      // If should be playing, play after load
      if (isPlaying) {
        audio.play().catch((error) => {
          console.error("Error playing audio:", error)
        })
      }
    }
  }, [src, isPlaying])

  // Handle play/pause state changes
  useEffect(() => {
    if (!audioRef.current) return

    const audio = audioRef.current

    if (isPlaying && audio.paused && audio.src) {
      // Resume if paused and should be playing
      audio.play().catch((error) => {
        console.error("Error playing audio:", error)
      })
    } else if (!isPlaying && !audio.paused) {
      // Pause if playing and should be paused
      audio.pause()
    }
  }, [isPlaying])

  // Listen to audio state changes and trigger onPauseChanged
  useEffect(() => {
    if (!audioRef.current) return

    const audio = audioRef.current

    const handlePlay = () => {
      onPauseChanged(false)
    }

    const handlePause = () => {
      onPauseChanged(true)
    }

    const handleEnded = () => {
      onPauseChanged(true)
    }

    audio.addEventListener("play", handlePlay)
    audio.addEventListener("pause", handlePause)
    audio.addEventListener("ended", handleEnded)

    return () => {
      audio.removeEventListener("play", handlePlay)
      audio.removeEventListener("pause", handlePause)
      audio.removeEventListener("ended", handleEnded)
    }
  }, [onPauseChanged])

  // Track time and duration updates with smooth animation
  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const updateProgress = () => {
      // Always access audioRef.current fresh to avoid stale closures
      const currentAudio = audioRef.current
      if (currentAudio && !currentAudio.paused) {
        setCurrentTime(currentAudio.currentTime)
        animationFrameRef.current = requestAnimationFrame(updateProgress)
      }
    }

    const startAnimationLoop = () => {
      // Cancel any existing frame before starting new one
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
      animationFrameRef.current = requestAnimationFrame(updateProgress)
    }

    const stopAnimationLoop = () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
        animationFrameRef.current = null
      }
    }

    const handleLoadedMetadata = () => {
      const currentAudio = audioRef.current
      if (currentAudio) {
        setDuration(currentAudio.duration)
        setCurrentTime(currentAudio.currentTime)
      }
    }

    const handleDurationChange = () => {
      const currentAudio = audioRef.current
      if (currentAudio) {
        setDuration(currentAudio.duration)
      }
    }

    const handlePlay = () => {
      startAnimationLoop()
    }

    const handlePause = () => {
      stopAnimationLoop()
      // Update one final time to show current position
      const currentAudio = audioRef.current
      if (currentAudio) {
        setCurrentTime(currentAudio.currentTime)
      }
    }

    // Fallback: timeupdate fires ~4 times per second and ensures progress updates
    // even when requestAnimationFrame stops (e.g., tab inactive)
    const handleTimeUpdate = () => {
      const currentAudio = audioRef.current
      if (currentAudio) {
        setCurrentTime(currentAudio.currentTime)
        // If animation frame isn't running but audio is playing, restart it
        if (!currentAudio.paused && !animationFrameRef.current) {
          startAnimationLoop()
        }
      }
    }

    const handleSeeked = () => {
      const currentAudio = audioRef.current
      if (currentAudio) {
        setCurrentTime(currentAudio.currentTime)
        // Restart animation if playing
        if (!currentAudio.paused) {
          startAnimationLoop()
        }
      }
    }

    audio.addEventListener("loadedmetadata", handleLoadedMetadata)
    audio.addEventListener("durationchange", handleDurationChange)
    audio.addEventListener("play", handlePlay)
    audio.addEventListener("pause", handlePause)
    audio.addEventListener("timeupdate", handleTimeUpdate)
    audio.addEventListener("seeked", handleSeeked)

    // Initialize values
    if (audio.duration && !isNaN(audio.duration)) {
      setDuration(audio.duration)
    }
    setCurrentTime(audio.currentTime)

    // Start animation if already playing
    if (!audio.paused) {
      startAnimationLoop()
    }

    return () => {
      audio.removeEventListener("loadedmetadata", handleLoadedMetadata)
      audio.removeEventListener("durationchange", handleDurationChange)
      audio.removeEventListener("play", handlePlay)
      audio.removeEventListener("pause", handlePause)
      audio.removeEventListener("timeupdate", handleTimeUpdate)
      audio.removeEventListener("seeked", handleSeeked)
      stopAnimationLoop()
    }
  }, [track?.id, track?.audio_url])

  const handleSeek = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!audioRef.current || !duration) return

    const rect = e.currentTarget.getBoundingClientRect()
    const x = e.clientX - rect.left
    const percentage = Math.max(0, Math.min(1, x / rect.width))
    const newTime = percentage * duration

    audioRef.current.currentTime = newTime
    setCurrentTime(newTime)
  }

  const progressPercentage = duration > 0 ? (currentTime / duration) * 100 : 0

  return (
    <>
      <audio ref={audioRef} className="hidden" />
      
      {/* Audio Bar - only show when playing */}
      {track && track.audio_url && (
        <div className="fixed bottom-0 left-0 right-0 z-50 bg-background border-t border-border shadow-lg">
          <div className="max-w-6xl mx-auto px-6 py-4">
            {/* Progress bar */}
            <div
              className="w-full h-2 bg-secondary rounded-full cursor-pointer mb-4 relative"
              onClick={handleSeek}
            >
              <div
                className="absolute top-0 left-0 h-full bg-primary rounded-full"
                style={{ width: `${Math.max(0, Math.min(100, progressPercentage))}%` }}
              />
            </div>

            {/* Controls */}
            <div className="flex items-center gap-4">
              {/* Track info */}
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-foreground truncate">
                  {track.name}
                </div>
                <div className="text-xs text-muted-foreground truncate">
                  {track.prompt}
                </div>
              </div>

              {/* Playback controls */}
              <div className="flex items-center gap-2">
                {onPrevious && (
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8"
                    onClick={onPrevious}
                  >
                    <SkipBack className="w-4 h-4" />
                  </Button>
                )}

                <Button
                  variant="default"
                  size="icon"
                  className="h-10 w-10 rounded-full"
                  onClick={onPlayPause}
                >
                  {isPlaying ? (
                    <Pause className="w-5 h-5" />
                  ) : (
                    <Play className="w-5 h-5 ml-0.5" />
                  )}
                </Button>

                {onNext && (
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8"
                    onClick={onNext}
                  >
                    <SkipForward className="w-4 h-4" />
                  </Button>
                )}
              </div>

              {/* Time display */}
              <div className="text-xs text-muted-foreground tabular-nums min-w-[100px] text-right">
                {formatTime(currentTime)} / {formatTime(duration)}
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
