import { useState, useEffect } from "react";
//import "@/styles/new.css"
import { Routes, Route, Link, Outlet } from 'react-router-dom';

import Header from "../components/custom/Header"
import Sidebar from "../components/custom/Sidebar"


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