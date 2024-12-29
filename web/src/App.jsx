import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useParams,
} from "react-router-dom";
import LoginPage from "./components/custom/LoginPage/LoginPage.jsx";
import RegisterPage from "./components/custom/RegisterPage/RegisterPage.jsx";
import EventListView from "./components/custom/EventListView.jsx";
import GameListView from "./components/custom/GameListView.jsx";
import LogListView from "./components/custom/LogListView.jsx";
import MainPage from "./pages/MainPage.jsx";
import NotFound from "./pages/NotFound.jsx";
import Dashboard from "./pages/Settings.jsx";
import AnnotationView from "./components/custom/AnnotationView/AnnotationView.jsx";
import ProtectedRoute from "./components/custom/ProtectedRoute";
import { Provider } from "react-redux";
import { PersistGate } from "redux-persist/integration/react";
import { store, persistor } from "./store";

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

const RedirectToImage = () => {
  const { id } = useParams();
  return <Navigate replace to={`/data/${id}/image/0`} />;
};

function App() {
  return (
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <BrowserRouter>
          <Routes>
            <Route
              path="/"
              element={
                <ProtectedRoute>
                  <MainPage />
                </ProtectedRoute>
              }
            >
              <Route index element={<EventListView />} />
              <Route
                path="/"
                element={
                  <ProtectedRoute>
                    <EventListView />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/events/:id"
                element={
                  <ProtectedRoute>
                    <GameListView />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/games/:id"
                element={
                  <ProtectedRoute>
                    <LogListView />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/settings"
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                }
              />
              {/* Redirect /data/:id to /data/:id/image/0 */}
              <Route
                path="/data/:id"
                element={
                  <ProtectedRoute>
                    <RedirectToImage />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/data/:id/image/:imageIndex"
                element={
                  <ProtectedRoute>
                    <AnnotationView />
                  </ProtectedRoute>
                }
              />
            </Route>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<RegisterPage />} />
            <Route path="/logout" element={<Logout />} />
            <Route path="*" element={<NotFound />}></Route>
          </Routes>
        </BrowserRouter>
      </PersistGate>
    </Provider>
  );
}

export default App;
