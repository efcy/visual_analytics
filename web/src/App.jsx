import { BrowserRouter, Routes, Route, Navigate, useParams } from "react-router-dom";
import LoginPage from "./pages/LoginPage.jsx";
import EventListView from "./components/custom/EventListView.jsx";
import GameListView from "./components/custom/GameListView.jsx";
import LogListView from "./components/custom/LogListView.jsx";
import EventPage from "./pages/EventPage.jsx";
import NotFound from "./pages/NotFound.jsx";
import Dashboard from "./pages/Settings.jsx";
import AnnotationView from "./components/custom/AnnotationView/AnnotationView.jsx";
import ProtectedRoute from "./components/custom/ProtectedRoute"
import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";
import { store, persistor } from "./store";


function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

const RedirectToImage = () => {
  const { id } = useParams();
  return <Navigate replace to={`/log/${id}/frame/1`} />;
};

function App() {
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <BrowserRouter>
          <Routes>
              
              <Route path="/" element={<ProtectedRoute><EventPage /></ProtectedRoute>}>
                <Route index element={<EventListView />} />
                <Route path="/" element={<ProtectedRoute><EventListView /></ProtectedRoute>} />
                <Route path="/events/:id" element={<ProtectedRoute><GameListView /></ProtectedRoute>} />
                <Route path="/games/:id" element={<ProtectedRoute><LogListView /></ProtectedRoute>} />
                <Route path="/settings" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
                {/* Redirect /log/:id to /log/:id/image/0 -  FIXME*/}
                <Route 
                  path="/log/:id" 
                  element={<ProtectedRoute><RedirectToImage /></ProtectedRoute>} 
                />
                <Route path="/log/:id/frame/:frameNumber" element={<ProtectedRoute><AnnotationView /></ProtectedRoute>} />
                
            </Route>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/logout" element={<Logout />} />
            <Route path="*" element={<NotFound />}></Route>
          </Routes>
        </BrowserRouter>
      </PersistGate>
    </Provider>
  );
}

export default App;
