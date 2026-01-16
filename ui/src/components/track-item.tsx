"use client"
import { Track } from "@/lib/types"
import { Button } from "./ui/button"
import { Progress } from "./ui/progress"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu"
import { Download, Pause, Play, Trash2, MoreVertical } from "lucide-react"
import { useEffect, useState } from "react"
import { observer } from "mobx-react-lite"
import { TrackStore } from "@/stores/track-store"
import { useTrackStore } from "@/stores/store-provider"

function formatTimeAgo(dateString: string): string {
    const seconds = Math.floor((new Date().getTime() - new Date(dateString).getTime()) / 1000)
    if (seconds < 60) return "just now"
    if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
    return `${Math.floor(seconds / 86400)}d ago`
}

interface TrackItemProps {
    track: Track
    isPlaying: boolean
    onClick: () => void
    onPlay: () => void
    onDelete?: () => void
}

const useTrackProgress = (track: Track) => {
    const store = useTrackStore()
    const currentStatus = store.getTrackJobStatus(track)
    const jobId = track.jobs[0].id

    useEffect(() => {
        if (!["completed", "failed"].includes(currentStatus)) {
            let isRunning = true
            let timeout: NodeJS.Timeout;

            const updateProgress = async () => {
                if (!isRunning) return
                await store.updateTrackProgress(jobId)


                if (!["completed", "failed"].includes(store.getTrackJobStatus(track))) {
                    timeout = setTimeout(async () => {
                        await updateProgress()
                    }, 3000)
                } else {
                    isRunning = false
                }
            }
            updateProgress()
            return () => { isRunning = false; clearTimeout(timeout) }
        }
    }, [currentStatus, store, jobId])

    return {
        currentStatus
    }
}

function TrackItemImpl({ track, isPlaying, onPlay, onClick, onDelete }: TrackItemProps) {
    const { currentStatus } = useTrackProgress(track)

    const handleDownload = (e: React.MouseEvent) => {
        e.stopPropagation()
        if (track.audio_url) {
            const link = document.createElement("a")
            link.href = track.audio_url
            link.download = `${track.name}.wav`
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
        }
    }

    return (
        <div
            key={track.id}
            onClick={() => onClick()}
            className={`flex items-center gap-4 p-4 transition-colors w-full ${currentStatus === "completed" ? "hover:bg-secondary/30 cursor-pointer" : ""
                }`}
        >
            <div className="p-4 bg-rose-300 rounded-sm flex items-center justify-center shrink-0 transition-colors">
            <button
                onClick={(e) => currentStatus === "completed" && onPlay()}
                disabled={currentStatus !== "completed"}
                className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 transition-colors ${currentStatus === "completed"
                    ? "bg-foreground text-background hover:bg-foreground/90"
                    : "bg-secondary text-muted-foreground"
                    }`}
            >
                {["processing", "pending"].includes(currentStatus) ? (
                    <div className="w-3 h-3 border-2 border-muted-foreground/30 border-t-muted-foreground rounded-full animate-spin" />
                ) : isPlaying ? (
                    <Pause className="w-3 h-3" />
                ) : (
                    <Play className="w-3 h-3 ml-0.5" />
                )}
            </button>
            </div>
            <div className="flex flex-col items-center gap-4 flex-1">
                <div className="w-full">
                    <div className="flex items-center justify-between gap-2">
                        <div className="flex items-center gap-4">
                        <span className="text-sm font-medium text-foreground truncate">{track.name}</span>
                        {currentStatus === "processing" && (
                            <span className="text-xs text-muted-foreground">{Math.round(track.jobs[0].progress)}%</span>
                        )}
                        </div>
                        <div className="hidden sm:flex items-center gap-2 text-xs text-muted-foreground">
                        <span className="flex-1">{track.category}</span>
                        <span className="w-10 tabular-nums">{track.duration}s</span>
                        {/* <span className="w-16">{formatTimeAgo(track.createdAt)}</span> */}
                            <DropdownMenu>
                                <DropdownMenuTrigger asChild>
                                    <Button
                                        variant="ghost"
                                        size="icon"
                                        className="h-8 w-8 text-muted-foreground hover:text-foreground"
                                        onClick={(e) => e.stopPropagation()}
                                    >
                                        <MoreVertical className="h-4 w-4" />
                                    </Button>
                                </DropdownMenuTrigger>
                                <DropdownMenuContent align="end" className="w-48">
                                    <DropdownMenuItem onClick={handleDownload} disabled={currentStatus !== "completed"}>
                                        <Download className="mr-2 h-4 w-4" />
                                        <span>Download</span>
                                    </DropdownMenuItem>
                                    {onDelete && (
                                        <>
                                            <DropdownMenuSeparator />
                                            <DropdownMenuItem
                                                onClick={(e: React.MouseEvent) => {
                                                    e.stopPropagation()
                                                    onDelete()
                                                }}
                                                className="text-destructive focus:text-destructive"
                                            >
                                                <Trash2 className="mr-2 h-4 w-4" />
                                                <span>Delete</span>
                                            </DropdownMenuItem>
                                        </>
                                    )}
                                </DropdownMenuContent>
                            </DropdownMenu>
                    </div>
                    </div>
                    <p className="text-xs text-muted-foreground line-clamp-1">{track.prompt}</p>
                </div>

                <div className=" w-full">
                    <Progress value={track.jobs[0].progress} className="h-1.5" />
                </div>
            </div>
        </div>
    )
}

export const TrackItem = observer(TrackItemImpl)