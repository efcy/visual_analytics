import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Login from "./pages/Login.jsx"
import EventListView from "./components/custom/EventListView.jsx"
import GameListView from "./components/custom/GameListView.jsx"
import LogListView from "./components/custom/LogListView.jsx"
import Register from "./pages/Register.jsx"
import EventPage from "./pages/EventPage.jsx"
import NotFound from "./pages/NotFound.jsx"
import Dashboard from "./pages/Settings.jsx"
import ProtectedRoute from "./components/custom/ProtectedRoute.jsx"
//import SingleImageViewer from "./components/custom/SingleImageViewer"
import CanvasImageViewer from "./components/custom/CanvasImageViewer.jsx"

function Logout() {
  localStorage.clear()
  return <Navigate to="/login" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

function App() {
  
  //<Route exact path="/" element={<Navigate to="/events" replace />}/>
  return (
    <BrowserRouter>
    
      <Routes>
      
        <Route path="/" element={<ProtectedRoute><EventPage /></ProtectedRoute>}>
          <Route index element={<EventListView />} />
          <Route path="/" element={<EventListView />} />
          <Route path="/events/:id" element={<GameListView />} />
          <Route path="/games/:id" element={<LogListView />} />
          <Route path="/settings" element={<Dashboard/>} />
          <Route path="/images/:id" element={<CanvasImageViewer/>} />
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
