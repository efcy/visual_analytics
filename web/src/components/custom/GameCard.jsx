import React from "react";
import "@/styles/new.css"

import event_image from '@/assets/robocup.jpeg';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card";
  import { Progress } from "@/components/ui/progress";

// TODO this should be a shadcn ui card component
function GameCard({ game }) {
    console.log("single game", game)
    return (
      <Card>
        <CardHeader>
          <img src={event_image} alt="" />
        </CardHeader>
        <CardContent>
          <CardTitle>{game ? game.team1 : ""} vs {game ? game.team2 : ""}</CardTitle>
          <p>
            Half: {game ? game.half : ""}
          </p>
          <p>
            Time: {game ? game.start_time : ""}
          </p>
        </CardContent>
        <CardFooter className="px-6">
          <Progress value={33} />
        </CardFooter>
      </Card>
    );
  }




export default GameCard