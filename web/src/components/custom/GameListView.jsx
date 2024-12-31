import { useState, useEffect } from "react";
import "@/styles/new.css";
import { useParams, Link } from "react-router-dom";
import api from "@/api";
import GameCard from "./GameCard/GameCard";
import { useDispatch } from "react-redux";
import { set_game, reset_game } from "@/reducers/breadcrumbSlice";

function LogListView() {
  const [games, setGames] = useState([]);
  const dispatch = useDispatch();
  const { id } = useParams();
  useEffect(() => {
    getGames();
  }, []); // this list is called dependency array

  const getGames = () => {
    //TODO enforce csrf in the backend and then add cockies here
    api
      .get(`${import.meta.env.VITE_API_URL}/api/games?event=${id}`)
      .then((res) => res.data)
      .then((data) => {
        setGames(data);
        console.log("Game List", data);
      })
      .catch((err) => alert(err));
    dispatch(reset_game());
  };

  const set_current_game = (game) => {
    var game_str = `${game.team1} vs ${game.team2} - ${game.half}`;
    dispatch(set_game(game_str));
  };

  return (
    <div className="projects-section">
      <div className="project-boxes jsGridView">
        {games.map((game) => (
          <Link
            to={`/games/${game.id}`}
            className="project-box-wrapper"
            key={game.id}
            onClick={() => set_current_game(game)}
          >
            <GameCard game={game} key={game.name}></GameCard>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default LogListView;
