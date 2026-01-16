"use client"

interface ProgressTrackerProps {
  progress: number
  trackName: string
}

export function ProgressTracker({ progress, trackName }: ProgressTrackerProps) {
  const stages = ["Analyzing", "Composing", "Processing", "Finalizing"]
  const currentStageIndex = Math.min(Math.floor(progress / 25), 3)

  return (
    <div className="border border-border rounded-lg p-6 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-foreground">{trackName}</p>
          <p className="text-xs text-muted-foreground">{stages[currentStageIndex]}</p>
        </div>
        <span className="text-sm font-mono text-muted-foreground">{Math.round(progress)}%</span>
      </div>

      {/* Progress bar */}
      <div className="h-1 bg-secondary rounded-full overflow-hidden">
        <div className="h-full bg-foreground transition-all duration-300 ease-out" style={{ width: `${progress}%` }} />
      </div>

      {/* Stage indicators */}
      <div className="flex justify-between">
        {stages.map((stage, index) => (
          <div key={stage} className="flex items-center gap-2">
            <div
              className={`w-1.5 h-1.5 rounded-full transition-colors ${
                index <= currentStageIndex ? "bg-foreground" : "bg-border"
              }`}
            />
            <span
              className={`text-xs ${
                index === currentStageIndex
                  ? "text-foreground"
                  : index < currentStageIndex
                    ? "text-muted-foreground"
                    : "text-muted-foreground/50"
              }`}
            >
              {stage}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}
