"use client"

import type React from "react"
import { useState } from "react"
import { observer } from "mobx-react-lite"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Slider } from "@/components/ui/slider"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { useTrackStore } from "@/stores/store-provider"

enum Models {
  small = "facebook/musicgen-small",
  medium = "facebook/musicgen-medium",
  large = "facebook/musicgen-large",
}

const modelOptions = Object.values(Models).map((model) => ({
  label: model,
  value: model,
}))

export const GenerationForm = observer(function GenerationForm() {
  const store = useTrackStore()

  const [prompt, setPrompt] = useState("")
  const [category, setCategory] = useState("")
  const [duration, setDuration] = useState([30])
  const [ model, setModel ] = useState(Models.small)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (prompt.trim()) {
      store.generate(prompt, category || "Uncategorized", duration[0], model)
      setPrompt("")
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight text-foreground">Generate</h1>
        <p className="text-sm text-muted-foreground mt-1">Describe the music you want to create</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6 grid">
        <Textarea
          placeholder="A calm piano melody with soft strings, suitable for a documentary about nature..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          className="min-h-[100px] bg-background border-border resize-none text-sm"
        />

        <div className="flex flex-col items-center gap-4">
          {/* <div className="flex-1 space-y-2">
              <label className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Category</label>
              <Select value={category} onValueChange={setCategory}>
                <SelectTrigger className="bg-background border-border h-9 text-sm">
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  {store.categories.map((cat) => (
                    <SelectItem key={cat.id} value={cat.name} className="text-sm">
                      {cat.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div> */}

            <div className="grid grid-cols-3 gap-8 w-full">
            <div className="flex-1 space-y-2">
              <label className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Category</label>
              <Select value={category} onValueChange={setCategory}>
                <SelectTrigger className="bg-background border-border h-9 text-sm w-full">
                  <SelectValue placeholder="Select category" />
                </SelectTrigger>
                <SelectContent>
                  {store.categories.map((cat) => (
                    <SelectItem key={cat.id} value={cat.name} className="text-sm">
                      {cat.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="w-full space-y-2">
              <label className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Model</label>
              <Select value={model} onValueChange={(value) => setModel(value as Models)}>
                <SelectTrigger className="bg-background border-border h-9 text-sm w-full">
                  <SelectValue placeholder="Select a model" />
                </SelectTrigger>
                <SelectContent>
                  {modelOptions.map((model) => (
                    <SelectItem key={model.value} value={model.value} className="text-sm">
                      {model.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

          <div className="w-full space-y-2">
            <label className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
              Duration: {duration[0]}s
            </label>
            <Slider value={duration} onValueChange={setDuration} max={120} min={5} step={1} className="py-2 mt-2" />
          </div>
          </div>

          <Button type="submit" disabled={!prompt.trim() || store.isGenerating} className="h-12 px-6 w-full">
            {store.isGenerating ? "Generating..." : "Generate"}
          </Button>
        </div>
      </form>
    </div>
  )
})
