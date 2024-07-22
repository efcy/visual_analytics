import react from 'react'
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/Login"
import EventListView from "./components/EventListView"
import GameListView from "./components/GameListView"
import Register from "./pages/Register"
import EventPage from "./pages/EventPage"
import NotFound from "./pages/NotFound"
import ProtectedRoute from "./components/ProtectedRoute"

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {
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
        <Route path="*" element={<NotFound />}></Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
