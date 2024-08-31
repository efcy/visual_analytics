import React from "react";

import { Link, } from "react-router-dom";
import { MdEvent } from "react-icons/md";
import { Button } from "@/components/ui/button";

// icon list: https://www.radix-ui.com/icons
import { GearIcon, ExitIcon } from "@radix-ui/react-icons"


function Sidebar() {
  return (
    <div className="app-sidebar">
      <Link to="/" className="app-sidebar-link">
        <MdEvent />
      </Link>
      <Button variant="ghost" size="icon" asChild>
        <Link to="/settings">
          <GearIcon className="h-4 w-4" />
        </Link>
      </Button>
      <Button variant="ghost" size="icon" asChild>
        <Link to="/logout">
          <ExitIcon className="h-4 w-4" />
        </Link>
      </Button>
    </div>
  );
}

export default Sidebar;
