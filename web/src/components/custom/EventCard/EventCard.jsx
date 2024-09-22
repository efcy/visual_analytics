import React from "react";
import "@/styles/new.css";
import DatePicker from "./DatePicker";
import MapComponent from "./MapComponent";
import event_image from "@/assets/robocup.jpeg";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import TimezonePicker from "@/components/custom/TimezonePicker/TimezonePicker.jsx";
import CountryPicker from "@/components/custom/CountryPicker/CountryPicker.jsx";
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { FaEllipsisV } from "react-icons/fa";
import { Progress } from "@/components/ui/progress";
import classes from "./EventCard.module.css";

// TODO have three dots here that open a context menu -> maybe open a dialog directly for editing the event
// could also open a drawer to the side for all the context (location, comments, number of games, etc)
// TODO add statistics here
function EventCard({ event, event_nav_func }) {
  return (
    <Card>
      <CardHeader onClick={() => event_nav_func(event)}>
        <img src={event_image} alt="" />
      </CardHeader>
      <CardContent>
        <div className={classes.card_title_wrapper}>
          <p className={classes.event_title}>Event: {event.name}</p>
          <Dialog className={classes.dialog}>
            <DialogTrigger>
              <FaEllipsisV />
            </DialogTrigger>
            <DialogContent>
              <div className={classes.dialog_wrapper}>
              <div className={classes.dialog_event_data}>
                <DialogHeader>
                  <DialogTitle>Update Event {event.name}</DialogTitle>
                  <DialogDescription></DialogDescription>
                </DialogHeader>
                <div className="p-0">
                  <div className="flex items-center mb-4">
                    <Label
                      htmlFor="event_name"
                      className="w-24 mr-4 text-right"
                    >
                      Name
                    </Label>
                    <Input placeholder="event_name" id="event_name" />
                  </div>
                  <div className="flex items-center mb-4">
                    <Label htmlFor="start_day" className="w-24 mr-4 text-right">
                      Start Day
                    </Label>
                    <DatePicker />
                  </div>
                  <div className="flex items-center mb-4">
                    <Label htmlFor="end_day" className="w-24 mr-4 text-right">
                      End Day
                    </Label>
                    <DatePicker />
                  </div>
                  <div className="flex items-center mb-4">
                    <Label htmlFor="timezone" className="w-24 mr-4 text-right">
                      Timezone
                    </Label>
                    <TimezonePicker />
                  </div>
                  <div className="flex items-center mb-4">
                    <Label htmlFor="country" className="w-24 mr-4 text-right">
                      Country
                    </Label>
                    <CountryPicker />
                  </div>
                  <div className="flex items-center mb-4">
                    <Label htmlFor="location" className="w-24 mr-4 text-right">
                      Location
                    </Label>
                    <Input placeholder="Location" id="location" />
                  </div>
                </div>
              </div>
              <MapComponent />
              </div>
            </DialogContent>
          </Dialog>
        </div>
        <p>
          <a
            target="_blank"
            rel="noopener noreferrer"
            href={`https://www.google.com/maps/place/${event.location}`}
            onClick={(e) => e.stopPropagation()} // Prevents parent navigation
          >
            Location
          </a>
        </p>
      </CardContent>
      <CardFooter className="px-6">
        <Progress value={33} />
      </CardFooter>
    </Card>
  );
}

export default EventCard;
