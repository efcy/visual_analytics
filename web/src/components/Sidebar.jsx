import React from "react";
import "../styles/new.css"
import { MdEvent, MdOutlineSettings  } from "react-icons/md";

function Sidebar() {
    return (
        <div className="app-sidebar">
            <a href="" className="app-sidebar-link">
                <MdEvent />
                
            </a>
            Events
            <a href="" className="app-sidebar-link">
                <MdOutlineSettings />
            </a>
            Settings
        </div>
    );
}

export default Sidebar