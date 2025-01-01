import { useGames } from "@/hooks/useGames";
import { useParams, Link } from "react-router-dom";

import GameCard from "../GameCard/GameCard.jsx";
import GridView from "../GridView/GridView.jsx";

function LogListView() {
  // get the event id from the url
  const { id } = useParams();
  // get the list of games for an event from the backend
  const games = useGames(id);

  if (!games) {
    // TODO make a better loading animation here
    return <div>Loading...</div>;
  }

  return (
    <GridView>
      {games.map((game) => (
        <Link to={`/games/${game.id}`} key={game.id}>
          <GameCard game={game} key={game.name}></GameCard>
        </Link>
      ))}
    </GridView>
  );
}

export default LogListView;
