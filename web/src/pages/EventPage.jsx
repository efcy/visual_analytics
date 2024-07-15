import { useState, useEffect } from "react";
import "../styles/new.css"
import { Routes, Route, Link, Outlet } from 'react-router-dom';

import Header from "../components/Header"
import Sidebar from "../components/Sidebar"


function EventPage() {

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