import React from "react";
import "../styles/new.css"
import { Routes, Route, Link, Outlet } from 'react-router-dom';
import { MdEvent, MdOutlineSettings  } from "react-icons/md";

function Sidebar() {
    return (
        <div className="app-sidebar">
            <Link to="/events" className="app-sidebar-link">
                <MdEvent />
            </Link>
        
            Events
            <a href="" className="app-sidebar-link">
                <MdOutlineSettings />
            </a>
            Settings
        </div>
    );
}

export default Sidebar