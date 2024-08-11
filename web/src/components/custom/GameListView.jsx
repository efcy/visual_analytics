import { useState, useEffect } from "react";
import "@/styles/new.css"
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import GameCard from "./GameCard"
import useDebounce from "@/hooks/use_debounce";
import { useDispatch } from "react-redux";
import { set_game, reset_game } from "@/reducers/breadcrumbSlice";

function LogListView() {
    const [games, setGames] = useState([]);
    const [searchtxt, setsearchtxt] = useState([]);
    const dispatch = useDispatch();
    const debounce = useDebounce(searchtxt, 300)
    const { id } = useParams();
    useEffect(() => {
        getGames();
    }, [debounce]); // this list is called dependency array

    const getGames = () => {
        //TODO enforce csrf in the backend and then add cockies here
        axios
            .get(`${import.meta.env.VITE_API_URL}/api/games?event=${id}`)
            .then((res) => res.data)
            .then((data) => {
                setGames(data);
                console.log("Game List", data);
            })
            .catch((err) => alert(err));
        dispatch(reset_game());
    };

    const set_current_game = (game) =>{
        var game_str =`${game.team1} vs ${game.team2} - ${game.half}`;
        dispatch(set_game(game_str));
    }
    
    return (
        <div className="projects-section">
            <div className="projects-section-line">
                <div className="search-wrapper">
                    <input className="search-input" type="text" placeholder="Search" />
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" className="feather feather-search" viewBox="0 0 24 24">
                        <defs></defs>
                        <circle cx="11" cy="11" r="8"></circle>
                        <path d="M21 21l-4.35-4.35"></path>
                    </svg>
                </div>
            </div>
            <div className="project-boxes jsGridView">
                {games.map((game) => (
                    <Link to={`/games/${game.id}`} className="project-box-wrapper" key={game.id} onClick={() => set_current_game(game)}>
                        <GameCard game={game} key={game.name}></GameCard>
                    </Link>
                ))}
            </div>
        </div>


    );
}

export default LogListView;

