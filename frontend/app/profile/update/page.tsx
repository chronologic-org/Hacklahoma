import Link from "next/link"
import Image from "next/image"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"

export default function UpdateProfilePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-200 via-cyan-200 to-green-200 p-4 md:p-8">
      <Card className="max-w-6xl mx-auto bg-[#FDE4CF]/90 rounded-xl">
        <div className="p-6">
          {/* Navigation */}
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-2xl font-bold">Chronologic</h1>
            <div className="flex gap-4">
            </div>
          </div>

          {/* Main content grid */}
          <div className="grid md:grid-cols-2 gap-8 ">
            {/* Left column */}
            <div className="space-y-6">
              <div>
                <h2 className="text-4xl font-bold mb-6">Updating Profile</h2>

                {/*Update the user's name*/}
                <div className="mb-4">
                  <label htmlFor="name" className="block mb-2">Name</label>
                  <input type="text" id="name" className="w-full rounded-xl p-2" />
                </div>
                <p className="text-xl text-gray-600">User Name: &lt;User Name&gt;</p>
              </div>

              <div className = "flex items-center justify-center gap-4">
                {/*Update the user's password*/}
                <Button className="bg-pink-100 hover:bg-pink-200">
                  <Link href="/updatePassword">Update Password</Link>
                </Button>
              </div>

              <Button className="bg-pink-100 hover:bg-pink-200">
                <Link href="/profile">Finish</Link>
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