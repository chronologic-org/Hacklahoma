import Link from "next/link"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

export default function Home() {
  return (
    <main className="min-h-screen gradient-bg p-4 md:p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <Card className="bg-[#90dbf4]/90 p-6">
          <h1 className="text-2xl font-bold mb-4">What is Chronologic?</h1>
          <p className="roboto-defultfont">
            Chronological is a service that connects to other commonly used software products to automatically build a
            tool for you to be able to disconnect from technology, without giving up the benefits of being connected.
          </p>
        </Card>

        <Card className="bg-[#fde4cf]/90 p-6">
          <h2 className="text-2xl font-bold mb-4">How do I use Chronologic?</h2>
          <p className="roboto-defultfont">
            In the Connections page two services can be connected by dragging them into the grid, or by selecting two
            services in the drop down menu. Once the services are connected you can enter your desired task into the
            input bar that appears.
          </p>
          <p className="roboto-defultfont mt-4">
            After the services are connected and the task is provided Chronologic will handle building the tool, and
            preforming the task.
          </p>
        </Card>

        <Card className="bg-[#b9fbc0]/90 p-6">
          <h2 className="text-2xl font-bold mb-4">Why use Chronologic?</h2>
          <p className="text-gray-800">
            The modern world has many software products that help you with your work or just consume your attention. But
            life does not wait for all these mundane tasks to be completed, time just continues anyway. Chronologic will
            help you disconnect from these time consuming tasks so you can get back to living.
          </p>
        </Card>

        <Card className="bg-[#98f5e1]/90 p-6 text-center">
          <h2 className="text-2xl font-bold mb-4">Get Started with Chronologic!</h2>
          <Link href="/connections">
            <Button className="bg-white text-black hover:bg-gray-100">Connections</Button>
          </Link>
        </Card>
      </div>
    </main>
  )
}

