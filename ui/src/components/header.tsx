"use client"

export function Header() {
  return (
    <header className="border-b border-border">
      <div className="max-w-6xl mx-auto px-6">
        <div className="flex items-center justify-between h-14">
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold tracking-tight text-foreground">MusicGen</span>
            <span className="text-xs text-muted-foreground">Studio</span>
          </div>

          <nav className="flex items-center gap-6">
            <a href="#" className="text-sm text-foreground">
              Generate
            </a>
            <a href="#" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Library
            </a>
            
          </nav>
        </div>
      </div>
    </header>
  )
}
