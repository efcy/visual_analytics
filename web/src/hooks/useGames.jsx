import { useState, useEffect, useDebugValue } from "react";
import api from "@/api";

export const useGames = (id) => {
  const [games, setGames] = useState(null);
  useDebugValue(games ? `${games}` : "Loading...");
  useEffect(() => {
    async function fetchGames() {
      api
        .get(`${import.meta.env.VITE_API_URL}/api/games?event=${id}`)
        .then((res) => res.data)
        .then((data) => {
          setGames(data);
        })
        .catch((err) => alert(err));
    }

    fetchGames();
  }, []);

  return games;
};
