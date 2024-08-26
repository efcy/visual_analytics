import "@/styles/globals.css";
import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

const Dashboard = () => {
  return (
    <div className="flex min-h-screen w-full flex-col projects-section">
      <main className="flex min-h-[calc(100vh_-_theme(spacing.16))] flex-1 flex-col gap-4 bg-muted/40 p-4 md:gap-8 md:p-10">
        <div className="mx-auto grid w-full max-w-6xl gap-2">
          <h1 className="text-3xl font-semibold">Settings</h1>
        </div>
        <div className="mx-auto grid w-full max-w-6xl items-start gap-6 md:grid-cols-[180px_1fr] lg:grid-cols-[400px_1fr]">
        <Card>
              <CardHeader>
                <CardTitle>Account info</CardTitle>
                <CardDescription></CardDescription>
              </CardHeader>
              <CardContent>
              <div className="p-0">
                <div className="flex items-center mb-4">
                <Label htmlFor="email" className="w-24 mr-4 text-right">Email</Label>
                <Input placeholder="Email" id="email" />
                </div>
                <div className="flex items-center mb-4">
                  <Label htmlFor="name" className="w-24 mr-4 text-right">First Name</Label>
                  <Input placeholder="First Name" id="name"/>
                </div>
                <div className="flex items-center mb-4">
                  <Label htmlFor="surname" className="w-24 mr-4 text-right">Last Name</Label>
                    <Input placeholder="Last Name" id="surname" />
                  </div>
                  </div>
              </CardContent>
              <CardFooter className="border-t px-6 py-4">
                <Button>Save</Button>
              </CardFooter>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Access Token</CardTitle>
                <CardDescription>
                  Use this token to authenticate with our API:
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form className="flex flex-col gap-4">
                  <Input
                    placeholder="Project Name"
                    defaultValue="Token"
                  />
                  <div className="flex items-center space-x-2">
                  <Button>Copy</Button>
                  <Button>Renew</Button>
                  </div>
                </form>
              </CardContent>
            </Card>
        </div>
      </main>
    </div>
  )
}

export default Dashboard;