import { useLogs } from "@/hooks/useLogs";
import { useParams, Link } from "react-router-dom";

import LogCard from "../LogCard/LogCard.jsx";
import GridView from "../GridView/GridView.jsx";

function LogListView() {
  // get the game id from the url
  const { id } = useParams();

  // get the list of games for an event from the backend
  const logs = useLogs(id);

  if (!logs) {
    // TODO make a better loading animation here
    return <div>Loading...</div>;
  }

  return (
    <GridView>
      {logs.map((log) => (
        <Link to={`/data/${log.id}`} key={log.id}>
          <LogCard log={log} key={log.name}></LogCard>
        </Link>
      ))}
    </GridView>
  );
}

export default LogListView;
