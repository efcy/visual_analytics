import { useState, useEffect } from "react";
import api from "@/api";
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
import { toast } from "sonner"

const Dashboard = () => {
  const [user, setUser] = useState('');
  const [first, setFirst] = useState('');
  const [last, setLast] = useState('');
  const [token, setToken] = useState(''); 
  const [email, setEmail] = useState('');
  const [copySuccess, setCopySuccess] = useState('');



  useEffect(() => {
    getUser();
    getToken();
    // Add an empty dependency array to avoid infinite calls
  }, []);


  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
      toast("Token has ben copied!")
      setCopySuccess('Copied!');
    } catch (err) {
      setCopySuccess('Failed to copy!');
    }
  };


  const getUser = () => {
    api
      .get(`${import.meta.env.VITE_API_URL}/accounts/user`)
      .then((res) => res.data)
      .then((data) => {
          setUser(data.username);
          setEmail(data.email);
          setFirst(data.first_name);
          setLast(data.last_name);
          console.log("User: ", data.username);
      })
      .catch((err) => alert(err));}
  
  const getToken = () => {
    api
      .get(`${import.meta.env.VITE_API_URL}/accounts/token`)
      .then((res) => res.data)
      .then((data) => {
          setToken(data.token);
          console.log("User: ", data.token);
      })
      .catch((err) => alert(err));}

  const handleNameChange = (e) => {
    setUser(e.target.value);
  };
  const handleEmailChange = (e) => {
    setEmail(e.target.value);
  };
  const handleFirstChange = (e) => {
    setFirst(e.target.value);
  };
  const handleLastChange = (e) => {
    setLast(e.target.value);
  };

  const updateUser = () => {
    const payload = {
      user_name: user,
      email: email,
      first_name:first,
      last_name:last
    };
    console.log("updating")
    api
      .put(`${import.meta.env.VITE_API_URL}/accounts/update`,payload)
      .then((res) => res.data)
      .catch((err) => alert(err));}
  
  
  const refreshToken = () => {
    api
      .get(`${import.meta.env.VITE_API_URL}/accounts/regentoken`)
      .then((res) => res.data)
      .then((data) => {
          setToken(data.token);
          console.log("User: ", data.token);
      })
      .catch((err) => alert(err));}


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
                <Label htmlFor="username" className="w-24 mr-4 text-right">Username</Label>
                <Input placeholder="username" id="username" value={user} onChange={handleNameChange} />
                </div>
                <div className="flex items-center mb-4">
                <Label htmlFor="email" className="w-24 mr-4 text-right">Email</Label>
                <Input placeholder="Email" id="email" value={email} onChange={handleEmailChange} />
                </div>
                <div className="flex items-center mb-4">
                  <Label htmlFor="name" className="w-24 mr-4 text-right">First Name</Label>
                  <Input placeholder="First Name" id="name" value={first} onChange={handleFirstChange}/>
                </div>
                <div className="flex items-center mb-4">
                  <Label htmlFor="surname" className="w-24 mr-4 text-right">Last Name</Label>
                    <Input placeholder="Last Name" id="surname" value={last} onChange={handleLastChange} />
                  </div>
                  </div>
              </CardContent>
              <CardFooter className="border-t px-6 py-4">
                <Button onClick={updateUser}>Save</Button>
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
                    disabled 
                    defaultValue={token}
                  />
                  <div className="flex items-center space-x-2">
                  <Button onClick={(e) => {
                    e.preventDefault(); 
                    copyToClipboard(token);
                  }}
                    >
                    Copy</Button>
                  <Button onClick={(e) => {
                      e.preventDefault(); // Prevent default form submission on button click
                      refreshToken();
                    }}
                  >
                    Renew
                  </Button>
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