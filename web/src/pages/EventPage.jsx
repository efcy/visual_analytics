import { Outlet } from 'react-router-dom';

import Header from "../components/custom/Header"
import Sidebar from "../components/custom/Sidebar/Sidebar.jsx"

function EventPage() {
  console.log("EventPage called")
  return (
    <div className="app-container">
      <Header />
      <div className="app-content">
        <Sidebar />
        <Outlet />
      </div>
    </div>
  );
}

export default EventPage;