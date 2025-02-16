"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { APICredentialsModal } from "@/components/api-credentials-modal"
import { ToolsModal } from "@/components/tools-modal"

export default function ConnectionsPage() {
  const [showAPIModal, setShowAPIModal] = useState(false)
  const [showToolsModal, setShowToolsModal] = useState(false)

  return (
    <div className="min-h-screen bg-[#ffcfd2] p-4">
      <div className="max-w-4xl mx-auto">
        <header className="flex justify-between items-center mb-6">
          <h1 className="text-2xl font-bold">Chronologic</h1>
          <Button variant="outline" onClick={() => setShowAPIModal(true)}>
            API Credentials
          </Button>
        </header>

        <main className="space-y-6">
          <div className="bg-white rounded-lg p-6 shadow-lg">
            <h2 className="text-lg font-semibold mb-4">Progress</h2>
            <div className="space-y-4">
              <div className="h-8 bg-gray-100 rounded"></div>
              <div className="h-8 bg-gray-100 rounded"></div>
            </div>
          </div>

          <div className="flex justify-between items-center gap-4">
            {/*below will need to pull the Left API*/}
            <div className="bg-[#fbf8cc] p-4 rounded-lg">Left API Name</div>
            {/*This is where the user inputs their connection*/}
            <Input placeholder="Enter your connection here..." className="flex-1" />
            {/*below will need to pull the Left API*/}
            <div className="bg-[#fbf8cc] p-4 rounded-lg">Right API Name</div>
          </div>

          <div className="fixed bottom-0 left-0 right-0 p-4 bg-white border-t">
            <div className="max-w-4xl mx-auto flex justify-between items-center">
              <Button variant="outline" onClick={() => setShowToolsModal(true)}>
                Tools
              </Button>
              <div className="flex gap-2">
                <div className="w-3 h-3 rounded-full bg-[#cfbaf0]"></div>
                <div className="w-3 h-3 rounded-full bg-[#a3c4f3]"></div>
                <div className="w-3 h-3 rounded-full bg-[#90dbf4]"></div>
                <div className="w-3 h-3 rounded-full bg-[#8eecf5]"></div>
              </div>
              <Button variant="outline">Clear</Button>
            </div>
          </div>
        </main>
      </div>

      <APICredentialsModal open={showAPIModal} onClose={() => setShowAPIModal(false)} />
      <ToolsModal open={showToolsModal} onClose={() => setShowToolsModal(false)} />
    </div>
  )
}

