import React, { useState, useEffect } from "react";
import EventBreadcrumb from "../EventBreadcrumb.jsx";

import classes from './Header.module.css'

function Header() {
  // State to track if the 'dark' class should be added
  const [isDarkMode, setIsDarkMode] = useState(false);

  // Effect to toggle the 'dark' class on the html element
  useEffect(() => {
    if (isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [isDarkMode]);

  const switchTheme = () => {
    setIsDarkMode(!isDarkMode);
  };
  return (
    <div className={classes.header}>
      <div className={classes.header_left}>
        <span className={classes.app_icon}></span>
        <EventBreadcrumb />
      </div>
      <div className={classes.header_right}>
        <button
          className={classes.mode_switch}
          title="Switch Theme"
          onClick={switchTheme}
        >
          <svg
            className="moon"
            fill="none"
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            width="24"
            height="24"
            viewBox="0 0 24 24"
          >
            <defs></defs>
            <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"></path>
          </svg>
        </button>
      </div>
    </div>
  );
}

export default Header;
