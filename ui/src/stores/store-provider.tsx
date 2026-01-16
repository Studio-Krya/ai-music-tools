"use client"

import { createContext, useContext, useEffect, type ReactNode } from "react"
import { trackStore } from "./track-store"

const StoreContext = createContext(trackStore)

export function StoreProvider({ children }: { children: ReactNode }) {
  useEffect(() => {
    trackStore.hydrate()
  }, [])

  return <StoreContext.Provider value={trackStore}>{children}</StoreContext.Provider>
}

export function useTrackStore() {
  return useContext(StoreContext)
}
