"use client"

import { useState } from "react"
import { observer } from "mobx-react-lite"
import { Plus, Pencil, Trash2, X, Check } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { useTrackStore } from "@/stores/store-provider"

const PRESET_COLORS = ["#6B7280", "#3B82F6", "#8B5CF6", "#F59E0B", "#10B981", "#EF4444", "#EC4899"]

export const CategoriesPanel = observer(function CategoriesPanel() {
  const store = useTrackStore()
  const [isAdding, setIsAdding] = useState(false)
  const [editingId, setEditingId] = useState<string | null>(null)
  const [newName, setNewName] = useState("")
  const [newColor, setNewColor] = useState(PRESET_COLORS[0])

  const handleAdd = () => {
    if (newName.trim()) {
      store.addCategory(newName.trim(), newColor)
      setNewName("")
      setNewColor(PRESET_COLORS[0])
      setIsAdding(false)
    }
  }

  const handleUpdate = (id: string) => {
    if (newName.trim()) {
      store.updateCategory(id, newName.trim(), newColor)
      setEditingId(null)
      setNewName("")
    }
  }

  const startEdit = (category: { id: string; name: string; color?: string }) => {
    setEditingId(category.id)
    setNewName(category.name)
    setNewColor(category.color || PRESET_COLORS[0])
  }

  return (
    <div className="space-y-8">
      {/* Stats */}
      <div>
        <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-3">Overview</p>
        <div className="space-y-2">
          <div className="flex justify-between items-baseline">
            <span className="text-sm text-muted-foreground">Total tracks</span>
            <span className="text-sm font-semibold tabular-nums">{store.tracks.length}</span>
          </div>
          {/* <div className="flex justify-between items-baseline">
            <span className="text-sm text-muted-foreground">Categories</span>
            <span className="text-2xl font-semibold tabular-nums">{store.categories.length}</span>
          </div> */}
        </div>
      </div>

      {/* Categories */}


      {/* Distribution */}
      <div>
        <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-3">Distribution</p>
        <div className="space-y-2">
          {
            store.getCategoryPercentages().map(({ name, percentage}) => {
              return (
                <div key={name} className="space-y-1">
                  <div className="flex justify-between text-xs">
                    <span className="text-muted-foreground">{name}</span>
                    <span className="text-muted-foreground tabular-nums">{Math.round(percentage)}%</span>
                  </div>
                  <div className="h-1 bg-secondary rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all"
                      style={{ width: `${percentage}%`, backgroundColor: PRESET_COLORS[0] }}
                    />
                  </div>
                </div>
              )
            })
          }
        </div>
      </div>
    </div>
  )
})
