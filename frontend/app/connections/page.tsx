"use client"

import Link from "next/link"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ToolsModal } from "@/components/tools-modal"
import { Loader2, Check, X } from "lucide-react"
import { Card } from "@/components/ui/card"

// Types
type Position = "left" | "right"
type PlacedItem = {
  id: string
  position: Position
  name: string
}
type PromptStatus = "running" | "completed" | "idle"
type Prompt = {
  text: string
  status: PromptStatus
}

// Constants
const POSITIONS = {
  left: { x: 250, y: 100 },
  right: { x: 550, y: 100 }
}

const ProgressItem = ({ prompt, onDelete }: { prompt: Prompt; onDelete?: () => void }) => (
  <div className="flex items-center gap-2">
    <div className="flex-1 h-8 bg-gray-100 rounded flex items-center px-3">
      {prompt.text}
    </div>
    <div className="w-8 flex justify-center">
      {prompt.status === "running" && (
        <Loader2 className="h-5 w-5 animate-spin text-gray-500" />
      )}
      {prompt.status === "completed" && (
        <div className="flex gap-2">
          <Check className="h-5 w-5 text-green-500" />
          {onDelete && (
            <X 
              className="h-5 w-5 text-red-500 cursor-pointer hover:text-red-600" 
              onClick={onDelete}
            />
          )}
        </div>
      )}
    </div>
  </div>
)

const Progress = ({ prompts, onDelete }: { prompts: Prompt[]; onDelete: (index: number) => void }) => (
  <div className="bg-white rounded-lg p-6 shadow-lg">
    <h2 className="text-lg font-semibold mb-4">Progress</h2>
    <div className="space-y-4">
      {prompts.map((prompt, index) => (
        <ProgressItem 
          key={index} 
          prompt={prompt} 
          onDelete={() => onDelete(index)}
        />
      ))}
    </div>
  </div>
)

const ClickableItem = ({ 
  id, 
  name, 
  onItemAdd,
  isPlaced,
  onRetrieve 
}: { 
  id: string
  name: string
  onItemAdd: (item: PlacedItem) => void
  isPlaced: boolean
  onRetrieve: (id: string) => void
}) => {
  const handleClick = () => {
    if (isPlaced) {
      onRetrieve(id)
      return
    }

    const newItem = {
      id,
      position: "left", // This will be determined by available position
      name,
    }

    // This is erroring, but it works in the app
    onItemAdd(newItem)
  }

  return (
    <div 
      onClick={handleClick}
      className={`p-2 ${isPlaced ? 'bg-gray-200 cursor-pointer' : 'bg-[#fbf8cc] hover:bg-[#f7f4b9] cursor-pointer'} rounded-lg transition-colors`}
    >
      {name}
    </div>
  )
}

const PlacedItem = ({ item }: { item: PlacedItem }) => {
  const position = POSITIONS[item.position]
  
  return (
    <div
      style={{
        position: 'absolute',
        left: position.x,
        top: position.y,
        transform: 'translate(-50%, -50%)',
      }}
      className="p-4 bg-[#8EECF5]/90 rounded-lg"
    >
      {item.name}
    </div>
  )
}

const Arrow = () => {
  const { x: x1, y: y1 } = POSITIONS.left
  const { x: x2, y: y2 } = POSITIONS.right
  
  return (
    <svg className="absolute inset-0 w-full h-full pointer-events-none">
      <defs>
        <marker
          id="arrowhead"
          viewBox="0 0 10 10"
          refX="5"
          refY="5"
          markerWidth="6"
          markerHeight="6"
          orient="auto-start-reverse"
        >
          <path d="M 0 0 L 10 5 L 0 10 z" fill="black"/>
        </marker>
      </defs>
      <path
        d={`M ${x1 + 60} ${y1} L ${x2 - 60} ${y2}`}
        stroke="black"
        strokeWidth="2"
        markerEnd="url(#arrowhead)"
        fill="none"
      />
    </svg>
  )
}

export default function ConnectionsPage() {
  const [showToolsModal, setShowToolsModal] = useState(false)
  const [placedItems, setPlacedItems] = useState<PlacedItem[]>([])
  const [connectionText, setConnectionText] = useState("")
  const [placedApis, setPlacedApis] = useState<Set<string>>(new Set())
  const [prompts, setPrompts] = useState<Prompt[]>([
    { text: "First prompt", status: "completed" },
    { text: "Second prompt", status: "running" }
  ])

  const getAvailablePosition = (): Position => {
    const positions = new Set(placedItems.map(item => item.position))
    return !positions.has("left") ? "left" : "right"
  }

  const handleAddItem = (newItem: PlacedItem) => {
    setPlacedItems(prev => {
      if (prev.length >= 2) return prev
      if (prev.some(i => i.id === newItem.id)) return prev
      
      newItem.position = getAvailablePosition()
      setPlacedApis(prevApis => new Set([...prevApis, newItem.id]))
      return [...prev, newItem]
    })
  }

  const handleRemoveItem = (id: string) => {
    setPlacedItems(prev => prev.filter(item => item.id !== id))
    setPlacedApis(prev => {
      const next = new Set(prev)
      next.delete(id)
      return next
    })
  }

  const handleClear = () => {
    setPlacedItems([])
    setConnectionText("")
    setPlacedApis(new Set())
  }

  const handleDeletePrompt = (index: number) => {
    setPrompts(prev => prev.filter((_, i) => i !== index))
  }

  return (
    <div className="min-h-screen bg-[#ffcfd2] p-4">
      <div className="max-w-4xl mx-auto">
      <header className="flex justify-between items-center px-6 mb-6">
        <h1 className="text-2xl font-bold">Chronologic</h1>
        <div className="flex gap-4">
          <Button className="bg-pink-100 hover:bg-pink-200">
            <Link href="/">Home</Link>
          </Button>
          <Button className="bg-pink-100 hover:bg-pink-200">
            <Link href="/logout">Log out</Link>
          </Button>
        </div>
      </header>


        <main className="space-y-6">
          <Progress prompts={prompts} onDelete={handleDeletePrompt} />

          <div className="relative h-[200px] bg-[#FCFBEF]/90 rounded-xl grid-area">
            {placedItems.length === 2 && <Arrow />}
            {placedItems.map((item) => (
              <PlacedItem key={item.id} item={item} />
            ))}
          </div>

          {placedItems.length === 2 && (
            <div className="flex justify-between items-center gap-4">
              <Card className=" bg-[#FCFBEF]/90 p-4 rounded-xl flex-1">
                <Input
                  placeholder="Enter your connection here..."
                  className="flex-1 rounded-xl"
                  value={connectionText}
                  onChange={(e) => setConnectionText(e.target.value)}
                />
              </Card>
            </div>
          )}
        </main>

        <div className="fixed bottom-0 left-0 right-0 p-4 bg-white border-t">
          <div className="max-w-4xl mx-auto flex justify-between items-center">
            <Button variant="outline" onClick={() => setShowToolsModal(true)}>
              Tools
            </Button>
            <div className="flex gap-4">
              <ClickableItem 
                id="left-api" 
                name="Left API" 
                isPlaced={placedApis.has("left-api")}
                onItemAdd={handleAddItem}
                onRetrieve={handleRemoveItem}
              />
              <ClickableItem 
                id="right-api" 
                name="Right API" 
                isPlaced={placedApis.has("right-api")}
                onItemAdd={handleAddItem}
                onRetrieve={handleRemoveItem}
              />
            </div>
            <Button variant="outline" onClick={handleClear}>
              Clear
            </Button>
          </div>
        </div>
      </div>

      <ToolsModal open={showToolsModal} onClose={() => setShowToolsModal(false)} />
    </div>
  )
}