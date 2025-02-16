import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import Image from "next/image"

export default function UpdateProfilePage() {
  return (
    <div className="min-h-screen gradient-bg p-4">
      <Card className="max-w-4xl mx-auto p-6">
        <div className="grid md:grid-cols-2 gap-8">
          <div className="space-y-6">
            <h1 className="text-2xl font-bold">Updating Profile</h1>

            <div className="space-y-4">
              <Input placeholder="Enter Name..." />
              {/* Placeholder for user name display -  needs backend integration to fetch actual user name */}
              <p>
                User Name: <span> </span>
              </p>{" "}
              {/* Replaced <User Name> with <span> and removed the erroneous closing tag */}
              <Button variant="outline" className="w-full">
                Update Password
              </Button>
            </div>

            <Button className="w-full">Finish</Button>
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

