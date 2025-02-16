import Link from "next/link"
import Image from "next/image"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export default function ProfilePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-200 via-cyan-200 to-green-200 p-4 md:p-8">
      <Card className="max-w-6xl mx-auto bg-[#FDE4CF]/90 rounded-xl">
        <div className="p-6">
          {/* Navigation */}
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-2xl font-bold">Chronologic</h1>
            <div className="flex gap-4">
              <Button className="bg-pink-100 hover:bg-pink-200">
                <Link href="/">Home</Link>
              </Button>
              <Button className="bg-pink-100 hover:bg-pink-200">
                <Link href="/connections">Connections</Link>
              </Button>
              <Button className="bg-pink-100 hover:bg-pink-200">
                <Link href="/logout">Log out</Link>
              </Button>
            </div>
          </div>

          {/* Main content grid */}
          <div className="grid md:grid-cols-2 gap-8 ">
            {/* Left column */}
            <div className="space-y-6">
              <div>
                <h2 className="text-4xl font-bold mb-6">Profile</h2>
                <p className="text-2xl mb-2">Hello, &lt;Name&gt;</p>
                <p className="text-xl text-gray-600">User Name: &lt;User Name&gt;</p>
              </div>

              <Card className=" p-6 bg-[#F1C0E8]/90 rounded-xl">
                <div className="space-y-4">
                  <div>
                    <h3 className="font-medium">Number of Tools Created:</h3>
                    <p>0</p>
                  </div>
                  <div>
                    <h3 className="font-medium">Date Joined:</h3>
                    <p>January 1, 2024</p>
                  </div>
                  <div>
                    <h3 className="font-medium">Connected Services</h3>
                    <p>None</p>
                  </div>
                </div>
              </Card>

              <Button className="bg-pink-100 hover:bg-pink-200">
                <Link href="/profile/update">Update</Link>
              </Button>
            </div>

            {/* Right column */}
            <div className="relative h-[400px] rounded-xl overflow-hidden bg-gradient-to-br from-blue-200 via-cyan-200 to-green-200">
              <div className="absolute inset-0 flex items-center justify-center">
                <Image
                  src="/placeholder.svg?height=200&width=200"
                  alt="Geometric pattern"
                  width={200}
                  height={200}
                  className="opacity-75"
                />
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  )
}