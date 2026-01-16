"use client"

import { observer } from "mobx-react-lite"
import { ProgressTracker } from "@/components/progress-tracker"
import { useTrackStore } from "@/stores/store-provider"

export const MainContent = observer(function MainContent() {
  const store = useTrackStore()

  if (!store.generatingTrack) {
    return null
  }

  return <ProgressTracker progress={store.currentProgress} trackName={store.generatingTrack.name} />
})
