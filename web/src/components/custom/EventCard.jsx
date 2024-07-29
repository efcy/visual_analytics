import React from "react";
import "@/styles/new.css";
import "@/styles/event.css";
import event_image from "@/assets/robocup.jpeg";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

// TODO have three dots here that open a context menu -> maybe open a dialog directly for editing the event
// could also open a drawer to the side for all the context (location, comments, number of games, etc)
// TODO add statistics here
function EventCard({ event }) {
  return (
    <Card>
      <CardHeader>
        <img src={event_image} alt="" />
      </CardHeader>
      <CardContent>
        <CardTitle>Event: {event.name}</CardTitle>
      </CardContent>
      <CardFooter className="px-6">
        <Progress value={33} />
      </CardFooter>
    </Card>
  );
}

export default EventCard;
