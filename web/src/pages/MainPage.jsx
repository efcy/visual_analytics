import { Outlet } from "react-router-dom";

import Header from "../components/custom/Header/Header.jsx";
import Sidebar from "../components/custom/Sidebar/Sidebar.jsx";

function MainPage() {
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

export default MainPage;
