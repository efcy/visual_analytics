import { useState, useEffect } from "react";
import "@/styles/new.css";
import { useParams, Link } from "react-router-dom";
import api from "@/api";
import GameCard from "./GameCard/GameCard";

function LogListView() {
  const [games, setGames] = useState([]);

  // get the event id from the url
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
  };

  return (
    <div className="projects-section">
      <div className="project-boxes jsGridView">
        {games.map((game) => (
          <Link
            to={`/games/${game.id}`}
            className="project-box-wrapper"
            key={game.id}
          >
            <GameCard game={game} key={game.name}></GameCard>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default LogListView;
