import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage.jsx";
import EventListView from "./components/custom/EventListView.jsx";
import GameListView from "./components/custom/GameListView.jsx";
import LogListView from "./components/custom/LogListView.jsx";
import Register from "./pages/Register.jsx";
import EventPage from "./pages/EventPage.jsx";
import NotFound from "./pages/NotFound.jsx";
import Dashboard from "./pages/Settings.jsx";
import ProtectedRoute from "./components/custom/ProtectedRoute.jsx";
import AnnotationView from "./components/custom/AnnotationView/AnnotationView.jsx";
import CanvasView from "./components/custom/CanvasView.jsx";


import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";
import { store, persistor } from "./store";

//Hack
import axios from "axios";
axios.defaults.withCredentials = true;

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

function App() {
  //<Route exact path="/" element={<Navigate to="/events" replace />}/>
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<EventPage />}>
              <Route index element={<EventListView />} />
              <Route path="/" element={<EventListView />} />
              <Route path="/events/:id" element={<GameListView />} />
              <Route path="/games/:id" element={<LogListView />} />
              <Route path="/settings" element={<Dashboard />} />
              <Route path="/images/:id" element={<AnnotationView />} />
            </Route>

            <Route path="/login" element={<LoginPage />} />
            <Route path="/logout" element={<Logout />} />
            <Route path="/register" element={<RegisterAndLogout />} />
            <Route path="*" element={<NotFound />}></Route>
          </Routes>
        </BrowserRouter>
      </PersistGate>
    </Provider>
  );
}

export default App;
