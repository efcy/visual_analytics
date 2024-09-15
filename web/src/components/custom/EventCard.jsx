import React from "react";
import "@/styles/new.css";

import event_image from "@/assets/robocup.jpeg";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

// TODO have three dots here that open a context menu -> maybe open a dialog directly for editing the event
// could also open a drawer to the side for all the context (location, comments, number of games, etc)
// TODO add statistics here
function EventCard({ event, event_nav_func  }) {
  return (
    <Card onClick={() => event_nav_func(event)}>
      <CardHeader>
        <img src={event_image} alt="" />
      </CardHeader>
      <CardContent>
        <CardTitle>Event: {event.name}</CardTitle>
        <p>
          <a target='_blank' 
          rel='noopener noreferrer' 
          href={`https://www.google.com/maps/place/${event.location}`}
          onClick={(e) => e.stopPropagation()} // Prevents parent navigation 
          >Location</a>
        </p>
      </CardContent>
      <CardFooter className="px-6">
        <Progress value={33} />
      </CardFooter>
    </Card>
  );
}

export default EventCard;
