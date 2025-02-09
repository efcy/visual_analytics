import React from "react";
import "@/styles/new.css";
import DatePicker from "../Datepicker/DatePicker";
import { ProgressBar } from "../ProgressBar/ProgressBar";
import MapComponent from "../MapView/MapComponent";
import event_image from "@/assets/robocup.jpeg";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import TimezonePicker from "@/components/custom/TimezonePicker/TimezonePicker.jsx";
import CountryPicker from "@/components/custom/CountryPicker/CountryPicker.jsx";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { FaEllipsisV } from "react-icons/fa";
import classes from "./EventCard.module.css";
import { cn } from "@/lib/utils";

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
          <Dialog>
            <DialogTrigger>
              <FaEllipsisV />
            </DialogTrigger>
            <DialogContent className={cn(classes.dialog)}>
              <div className={classes.dialog_wrapper}>
                <div className={classes.dialog_event_data}>
                  <DialogHeader>
                    <DialogTitle>Update Event {event.name}</DialogTitle>
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
                      <Label
                        htmlFor="start_day"
                        className="w-24 mr-4 text-right"
                      >
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
                      <Label
                        htmlFor="timezone"
                        className="w-24 mr-4 text-right"
                      >
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
                      <Label
                        htmlFor="location"
                        className="w-24 mr-4 text-right"
                      >
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
        <ProgressBar value={40} />
      </CardFooter>
    </Card>
  );
}

export default EventCard;
