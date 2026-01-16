export interface Track {
  id: string
  name: string
  prompt: string
  description?: string
  duration: number
  category?: string
  audio_url?: string
  jobs: Job[]
}

export interface Job {
  id: string
  track_id: string
  status: "pending" | "processing" | "completed" | "failed"
  progress: number
  artifact_url?: string
}

export interface Category {
  id: string
  name: string
  count: number
  color?: string
}
