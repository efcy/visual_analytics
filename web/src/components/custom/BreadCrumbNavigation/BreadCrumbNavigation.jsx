import { useLocation } from "react-router-dom";
import { useGames } from "@/hooks/useGames";
import { useLog, useLogs } from "@/hooks/useLogs";

import classes from "./BreadCrumbNavigation.module.css";

const BreadCrumbNavigation = () => {
  const location = useLocation();
  console.log("location:", location);

  const getBreadcrumbs = () => {
    const path = location.pathname;
    var my_array = [];
    // Handle root path
    if (path === "/") {
      return ["Startpage"];
    }

    // Split path and remove empty strings
    const segments = path.split("/").filter(Boolean);

    // Handle specific routes with IDs
    const [route, id] = segments;

    if (route === "events") {
      console.log("handle events route");
      const games = useGames(id);
      if (!games) {
        // TODO make a better loading animation here
        return my_array;
      }
      my_array.push("Event");
      my_array.push(`${games[0].event_name}`);
    }
    if (route === "games") {
      console.log("handle games route");
      const logs = useLogs(id);
      if (!logs) {
        // TODO make a better loading animation here
        return my_array;
      }
      my_array.push("Event");
      my_array.push(`${logs[0].event_name}`);
      my_array.push("Game");
      my_array.push(`${logs[0].game_name}`);
      return my_array;
    }
    if (route === "data") {
      console.log("handle data route");
      const log = useLog(id);
      if (!log) {
        // TODO make a better loading animation here
        return my_array;
      }
      console.log(log);
      my_array.push("Event");
      my_array.push(`${log.event_name}`);
      my_array.push("Game");
      my_array.push(`${log.game_name}`);
      my_array.push("Log");
      my_array.push(`${log.player_number}-${log.head_number}`);
    }

    return my_array;
  };

  const mycoolVar = getBreadcrumbs();
  console.log("blabla: ", mycoolVar);

  return (
    <ol className={classes.breadcrumb}>
      {mycoolVar.map((text, index) => (
        <li key={index}>{text}</li>
      ))}
    </ol>
  );
};

export default BreadCrumbNavigation;
