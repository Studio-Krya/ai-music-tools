import { makeAutoObservable, runInAction } from "mobx"
import type { Track, Category, Job } from "@/lib/types"
import { uniqueNamesGenerator, adjectives, colors, animals, languages } from 'unique-names-generator';

const STORAGE_KEY = "musicgen_tracks"
const CATEGORIES_KEY = "musicgen_categories"
const BASE_URL = "http://localhost:8000"
const defaultCategories: Category[] = [
  { id: "1", name: "Ambient", count: 0, color: "#6B7280" },
  { id: "2", name: "Electronic", count: 0, color: "#3B82F6" },
  { id: "3", name: "Cinematic", count: 0, color: "#8B5CF6" },
  { id: "4", name: "Lo-Fi", count: 0, color: "#F59E0B" },
  { id: "5", name: "Jazz", count: 0, color: "#10B981" },
]

export class TrackStore {
  tracks: Track[] = []
  activeCategory: string | null = null
  isGenerating = false

  constructor() {
    makeAutoObservable(this)
  }

  // Hydrate from localStorage (call on client only)
  async hydrate() {
    if (typeof window === "undefined") return

    const storedTracks = await fetch(`http://localhost:8000/tracks`).then(res => res.json())

    if (storedTracks) {
      this.tracks = storedTracks.map((track: Track) => ({
        ...track,
        audio_url: `${BASE_URL}${track.jobs[0].artifact_url}`,
      }))
    }

  }

  // Persist to localStorage
  private persist() {
    if (typeof window === "undefined") return
    // localStorage.setItem(STORAGE_KEY, JSON.stringify(this.tracks))
    // localStorage.setItem(CATEGORIES_KEY, JSON.stringify(this.categories))
  }


  getCategoryPercentages() {
    const categoryMap = new Map<string, number>()
    this.tracks.forEach((track) => {
      const category = track.category ?? "Uncategorized"
      categoryMap.set(category, (categoryMap.get(category) || 0) + 1)
    })

    return Array.from(categoryMap.entries()).map(([category, count]) => ({
      name: category,
      percentage: count / this.tracks.length * 100,
    }))
  }
 
  getTrackById(id: string): Track | undefined {
    return this.tracks.find((t) => t.id === id)
  }

  updateTrackName(id: string, name: string) {
    const track = this.tracks.find((t) => t.id === id)
    if (track) {
      track.name = name
      this.persist()
    }
  }

  get filteredTracks() {
    return this.tracks
  }
  
  async generate(prompt: string, category: string, duration: number, model: string) {
    if (this.isGenerating) return

    runInAction(() => {
      this.isGenerating = true
    })

    await this.addTrack(prompt, category, duration, model)

    runInAction(() => {
      this.isGenerating = false
    })
  }

  async addTrack(prompt: string, category: string, duration: number, model: string) {

    const name = uniqueNamesGenerator({ dictionaries: [adjectives, colors, adjectives, animals], separator: ' ', length: 4, style: 'capital' });
    const response = await fetch("http://localhost:8000/tracks", {
      method: "POST",
      body: JSON.stringify({ prompt: prompt, duration, category, name, model, provider: 'audiocraft' }),
      headers: {
        "Content-Type": "application/json",
      },
    })

    if (!response.ok) {
      throw new Error("Failed to generate audio")
    }

    const newTrack: Track = await response.json()
    newTrack.audio_url = `${BASE_URL}${newTrack.jobs[0].artifact_url}`

    this.tracks.unshift(newTrack)
  }

  async updateTrackProgress(jobId: string) {
    const response = await fetch(`http://localhost:8000/tracks/jobs/${jobId}`)
    if (!response.ok) {
      throw new Error("Failed to check progress")
    }

    const data: Job = await response.json()
    const trackId = data.track_id
    const progress = data.progress
    const status = data.status

    const track = this.tracks.find((t) => t.id === trackId)
    const job =track?.jobs.find((j) => j.id === jobId)

    if(job && track) {
      runInAction(() => {
        job.progress = progress
        job.status = status
        job.artifact_url = data.artifact_url ? `${BASE_URL}${data.artifact_url}` : undefined
        track.audio_url = data.artifact_url ? `${BASE_URL}${data.artifact_url}` : undefined
      })
    }
  }

  getTrackJobStatus(track: Track) {
    return track.jobs[0].status ?? "pending"
  }

  
  // deleteTrack(id: string) {
  //   const track = this.tracks.find((t) => t.id === id)
  //   if (track && track.status === "success") {
  //     const category = this.categories.find((c) => c.name === track.category)
  //     if (category && category.count > 0) {
  //       category.count--
  //     }
  //   }
  //   this.tracks = this.tracks.filter((t) => t.id !== id)
  //   this.persist()
  // }


  // stopGeneration() {
  //   this.isGenerating = false
  // }
}

// Singleton instance
export const trackStore = new TrackStore()
