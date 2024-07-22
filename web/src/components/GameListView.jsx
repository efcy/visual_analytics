import { useState, useEffect } from "react";
import "../styles/new.css"
import { useParams, Link } from 'react-router-dom';

import Event from "../components/Event"
import api from "../api";
import useDebounce from "../hooks/use_debounce";


function GameListView() {
    const [games, setGames] = useState([]);
    const [searchtxt, setsearchtxt] = useState([]);

    const debounce = useDebounce(searchtxt, 300)
    const { id } = useParams();
    useEffect(() => {
        getGames();
    }, [debounce]); // this list is called dependency array

    const getGames = () => {
        api
            .get(`/api/games?event=${id}`)
            .then((res) => res.data)
            .then((data) => {
                setGames(data);
                console.log("Game List", data);
            })
            .catch((err) => alert(err));
    };


    
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
                    <Link to={`/events/${game.id}`} className="project-box-wrapper" key={game.id}>
                        <Event event={game} key={game.name}></Event>
                    </Link>
                ))}
            </div>
        </div>


    );
}

export default GameListView;

