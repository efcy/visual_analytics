import "@/styles/new.css";

import event_image from "@/assets/robocup.jpeg";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ProgressBar } from "../ProgressBar/ProgressBar";
// TODO this should be a shadcn ui card component

function LogCard({ log }) {
  console.log("LogCard:", log);
  return (
    <Card>
      <CardHeader>
        <img src={event_image} alt="" />
      </CardHeader>
      <CardContent>
        <CardTitle>
          Player number: {log ? log.player_number : ""}
          <br />
          Head number: {log ? log.head_number : ""}
        </CardTitle>
      </CardContent>
      <CardFooter className="px-6">
        <ProgressBar value={33} />
      </CardFooter>
    </Card>
  );
}

export default LogCard;
