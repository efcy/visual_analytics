import react from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/Login"
import EventListView from "./components/EventListView"
import GameListView from "./components/GameListView"
import Register from "./pages/Register"
import EventPage from "./pages/EventPage"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"
import SingleImageViewer from "./components/SingleImageViewer"
import CanvasImageViewer from "./components/CanvasImageViewer"

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

  return (
    <BrowserRouter>
      <Routes>
      <Route exact path="/" element={<Navigate to="/events" replace />}/>
        <Route path="/events" element={<ProtectedRoute><EventPage /></ProtectedRoute>}>
          <Route index element={<EventListView />} />
          <Route path="/events/" element={<EventListView />} />
          <Route path="/events/:id" element={<GameListView />} />
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
