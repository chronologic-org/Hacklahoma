import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import Image from "next/image"

export default function ProfilePage() {
  const userName = "John Doe" // Example user name, replace with actual data fetching
  return (
    <div className="min-h-screen gradient-bg p-4">
      <Card className="max-w-4xl mx-auto p-6">
        <div className="grid md:grid-cols-2 gap-8">
          <div className="space-y-6">
            <h1 className="text-2xl font-bold">Profile</h1>

            <div>
              <h2 className="text-lg mb-2">Hello, {userName}</h2>
              <p>User Name: {userName}</p>
            </div>

            <div>
              <p>Number of Tools Created: 0</p> {/* Placeholder data */}
              <p>Date Joined: 2024-07-26</p> {/* Placeholder data */}
              <p>Connected Services</p>
            </div>

            <Button className="w-full">Update</Button>
          </div>

          <div className="flex items-center justify-center">
            <div className="w-48 h-48 relative">
              <Image
                src="/placeholder.svg?height=192&width=192"
                alt="Profile logo"
                width={192}
                height={192}
                className="object-contain"
              />
            </div>
          </div>
        </div>
      </Card>
    </div>
  )
}

