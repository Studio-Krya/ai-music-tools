"use client"

import { useEffect, useState, use } from "react"
import { observer } from "mobx-react-lite"
import { useRouter } from "next/navigation"
import { ArrowLeft, Play, Pause, Download, Trash2, Pencil, Check, X } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useTrackStore } from "@/stores/store-provider"
import type { Track } from "@/lib/types"

function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

function TrackDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params)
  const store = useTrackStore()
  const router = useRouter()
  const [track, setTrack] = useState<Track | undefined>(undefined)
  const [isPlaying, setIsPlaying] = useState(false)
  const [isEditingName, setIsEditingName] = useState(false)
  const [editedName, setEditedName] = useState("")
  const [currentTime, setCurrentTime] = useState(0)

  useEffect(() => {
    const foundTrack = store.getTrackById(id)
    if (foundTrack) {
      setTrack(foundTrack)
      setEditedName(foundTrack.name)
    }
  }, [id, store, store.tracks])

  const handleSaveName = () => {
    if (editedName.trim() && track) {
      store.updateTrackName(track.id, editedName.trim())
      setIsEditingName(false)
    }
  }

  const handleCategoryChange = (newCategory: string) => {
    if (track) {
      store.updateTrackCategory(track.id, newCategory)
    }
  }

  const handleDelete = () => {
    if (track) {
      store.deleteTrack(track.id)
      router.push("/")
    }
  }

  const togglePlay = () => {
    setIsPlaying(!isPlaying)
    // Simulate playback progress
    if (!isPlaying) {
      const interval = setInterval(() => {
        setCurrentTime((prev) => {
          if (prev >= (track?.duration || 30)) {
            clearInterval(interval)
            setIsPlaying(false)
            return 0
          }
          return prev + 0.1
        })
      }, 100)
    }
  }

  if (!track) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <p className="text-muted-foreground">Track not found</p>
          <Button variant="ghost" className="mt-4" onClick={() => router.push("/")}>
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to library
          </Button>
        </div>
      </div>
    )
  }

  const progress = (currentTime / track.duration) * 100

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-3xl mx-auto px-6 py-8">
        {/* Header */}
        <div className="mb-8">
          <Button
            variant="ghost"
            size="sm"
            className="text-muted-foreground -ml-2 mb-4"
            onClick={() => router.push("/")}
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back
          </Button>
        </div>

        {/* Track Info */}
        <div className="space-y-8">
          {/* Title */}
          <div>
            {isEditingName ? (
              <div className="flex items-center gap-2">
                <Input
                  value={editedName}
                  onChange={(e) => setEditedName(e.target.value)}
                  className="text-2xl font-semibold h-auto py-1 px-2"
                  autoFocus
                  onKeyDown={(e) => e.key === "Enter" && handleSaveName()}
                />
                <Button variant="ghost" size="icon" onClick={() => setIsEditingName(false)}>
                  <X className="w-4 h-4" />
                </Button>
                <Button variant="ghost" size="icon" onClick={handleSaveName}>
                  <Check className="w-4 h-4" />
                </Button>
              </div>
            ) : (
              <div className="flex items-center gap-2 group">
                <h1 className="text-2xl font-semibold text-foreground">{track.name}</h1>
                <Button
                  variant="ghost"
                  size="icon"
                  className="h-8 w-8 opacity-0 group-hover:opacity-100 transition-opacity"
                  onClick={() => setIsEditingName(true)}
                >
                  <Pencil className="w-4 h-4" />
                </Button>
              </div>
            )}
          </div>

          {/* Player */}
          <div className="border border-border rounded-lg p-6 space-y-6">
            {/* Waveform placeholder */}
            <div className="relative h-24 bg-secondary/30 rounded-md overflow-hidden">
              <div className="absolute inset-0 flex items-center justify-center gap-0.5">
                {Array.from({ length: 80 }).map((_, i) => {
                  const height = Math.random() * 60 + 20
                  const isPlayed = (i / 80) * 100 < progress
                  return (
                    <div
                      key={i}
                      className={`w-1 rounded-full transition-colors ${isPlayed ? "bg-foreground" : "bg-muted-foreground/30"}`}
                      style={{ height: `${height}%` }}
                    />
                  )
                })}
              </div>
              {/* Progress overlay */}
              <div
                className="absolute top-0 left-0 h-full bg-foreground/5 pointer-events-none"
                style={{ width: `${progress}%` }}
              />
            </div>

            {/* Controls */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <button
                  onClick={togglePlay}
                  className="w-12 h-12 rounded-full bg-foreground text-background flex items-center justify-center hover:bg-foreground/90 transition-colors"
                >
                  {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5 ml-0.5" />}
                </button>
                <div className="text-sm tabular-nums text-muted-foreground">
                  {Math.floor(currentTime)}:{String(Math.floor((currentTime % 1) * 10)).padStart(1, "0")}
                  <span className="mx-1">/</span>
                  {track.duration}:0
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="outline" size="sm">
                  <Download className="w-4 h-4 mr-2" />
                  Download
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="text-destructive hover:text-destructive bg-transparent"
                  onClick={handleDelete}
                >
                  <Trash2 className="w-4 h-4 mr-2" />
                  Delete
                </Button>
              </div>
            </div>
          </div>

          {/* Details */}
          <div className="grid grid-cols-2 gap-6">
            <div className="space-y-4">
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Prompt</p>
                <p className="text-sm text-foreground">{track.prompt}</p>
              </div>
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Created</p>
                <p className="text-sm text-foreground">{formatDate(track.createdAt)}</p>
              </div>
            </div>
            <div className="space-y-4">
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Category</p>
                <Select value={track.category} onValueChange={handleCategoryChange}>
                  <SelectTrigger className="w-full h-9">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {store.categories.map((cat) => (
                      <SelectItem key={cat.id} value={cat.name}>
                        <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full" style={{ backgroundColor: cat.color }} />
                          {cat.name}
                        </div>
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Duration</p>
                <p className="text-sm text-foreground">{track.duration} seconds</p>
              </div>
              <div>
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Status</p>
                <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                  {track.status}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

const TrackDetail = observer(TrackDetailPage)
export default TrackDetail
