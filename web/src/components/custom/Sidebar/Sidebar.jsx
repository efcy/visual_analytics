import React from "react";
import { Link, } from "react-router-dom";
import { MdEvent } from "react-icons/md";
import { Button } from "@/components/ui/button";

// icon list: https://www.radix-ui.com/icons
import { GearIcon, ExitIcon } from "@radix-ui/react-icons"
import classes from './Sidebar.module.css'

function Sidebar() {
  return (
    <div className={classes.sidebar}>
      <Link to="/" className={classes.sidebar_link}>
        <MdEvent />
      </Link>
      <Button variant="ghost" size="icon" asChild>
        <Link to="/settings" className={classes.sidebar_link}>
          <GearIcon className="h-4 w-4" />
        </Link>
      </Button>
      <Button variant="ghost" size="icon" asChild>
        <Link to="/logout" className={classes.sidebar_link}>
          <ExitIcon className="h-4 w-4" />
        </Link>
      </Button>
    </div>
  );
}

export default Sidebar;
