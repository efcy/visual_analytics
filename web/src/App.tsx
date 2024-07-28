import react from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/Login"
import EventListView from "./components/custom/EventListView"
import GameListView from "./components/custom/GameListView"
import Register from "./pages/Register"
import EventPage from "./pages/EventPage"
import NotFound from "./pages/NotFound"
import Dashboard from "./pages/Settings"
import ProtectedRoute from "./components/custom/ProtectedRoute"
import SingleImageViewer from "./components/custom/SingleImageViewer"
import CanvasImageViewer from "./components/custom/CanvasImageViewer"

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {
  const yourArrayOfImageUrls = [
    "https://logs.naoth.de/2024-04-17_GO24/2024-04-18_13-50-00_Berlin%20United_vs_Hulks_half2/extracted/1_15_Nao0006_240418-1243/log_top/0000001.png",
    "https://logs.naoth.de/2024-04-17_GO24/2024-04-18_13-50-00_Berlin%20United_vs_Hulks_half2/extracted/1_15_Nao0006_240418-1243/log_top/0021136.png"
  ];
  //<Route exact path="/" element={<Navigate to="/events" replace />}/>
  return (
    <BrowserRouter>
    
      <Routes>
      
        <Route path="/" element={<ProtectedRoute><EventPage /></ProtectedRoute>}>
          <Route index element={<EventListView />} />
          <Route path="/" element={<EventListView />} />
          <Route path="/events/:id" element={<GameListView />} />
          <Route path="/settings" element={<Dashboard/>} />
        </Route>
        
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="/test" element={<CanvasImageViewer imageUrls={yourArrayOfImageUrls}/>} />
        <Route path="*" element={<NotFound />}></Route>
        
      </Routes>
    </BrowserRouter>
  )
}

export default App
