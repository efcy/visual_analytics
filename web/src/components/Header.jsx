import React, { useState, useEffect } from 'react';
import "../styles/new.css"



function Header() {
    // State to track if the 'dark' class should be added
    const [isDarkMode, setIsDarkMode] = useState(false);

    // Effect to toggle the 'dark' class on the html element
    useEffect(() => {
        if (isDarkMode) {
        document.documentElement.classList.add('dark');
        } else {
        document.documentElement.classList.remove('dark');
        }
    }, [isDarkMode]);

    const switchTheme = () => {
        setIsDarkMode(!isDarkMode);
    }
    return (
        <div className="app-header">
            <div className="app-header-left">
                <span className="app-icon"></span>
                <p className="app-name">Events</p>

            </div>
            <div className="app-header-right">
                <button className="add-btn" title="Add New Project">
                    <svg className="btn-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" className="feather feather-plus">
                        <line x1="12" y1="5" x2="12" y2="19" />
                        <line x1="5" y1="12" x2="19" y2="12" /></svg>
                </button>
                <button className="mode-switch" title="Switch Theme" onClick={switchTheme}>
                    <svg className="moon" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" width="24" height="24" viewBox="0 0 24 24">
                        <defs></defs>
                        <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"></path>
                    </svg>
                </button>

                <button className="notification-btn">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="feather feather-bell">
                        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
                        <path d="M13.73 21a2 2 0 0 1-3.46 0" /></svg>
                </button>
            </div>
        </div>
    );
}

export default Header