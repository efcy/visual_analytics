import React from "react";
import "@/styles/new.css";
import { Routes, Route, Link, Outlet } from "react-router-dom";
import { MdEvent, MdOutlineSettings } from "react-icons/md";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
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

function Sidebar_w_dialog() {
  return (
    <div className="app-sidebar">
      <Link to="/" className="app-sidebar-link">
        <MdEvent />
      </Link>
      Events
      <a href="" className="app-sidebar-link">
        <MdOutlineSettings />
      </a>
      Settings
      <Dialog>
        <DialogTrigger asChild>
          <Button variant="ghost" size="icon">
            <GearIcon className="h-4 w-4" />
          </Button>
          
        </DialogTrigger>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Are you sure absolutely sure?</DialogTitle>
            <DialogDescription>
              This action cannot be undone. This will permanently delete your
              account and remove your data from our servers.
            </DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default Sidebar;
