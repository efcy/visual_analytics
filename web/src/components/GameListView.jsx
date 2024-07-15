import { useState, useEffect } from "react";
import "../styles/new.css"
import {useParams } from 'react-router-dom';

import Event from "../components/Event"


function GameListView() {
    const { id } = useParams();
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
                <h1>Games for Event {id}</h1>
            </div>
        </div>


    );
}

export default GameListView;

