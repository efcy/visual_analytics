import { useState, useEffect } from "react";
import "@/styles/new.css"
import { useParams, Link } from 'react-router-dom';

import LogCard from "./LogCard"
import api from "@/api";
import useDebounce from "@/hooks/use_debounce";


function LogListView() {
    const [logs, setLogs] = useState([]);
    const [searchtxt, setsearchtxt] = useState([]);

    const debounce = useDebounce(searchtxt, 300)
    const { id } = useParams();
    useEffect(() => {
        getLogs();
    }, [debounce]); // this list is called dependency array

    const getLogs = () => {
        api
            .get(`/api/logs?game=${id}`)
            .then((res) => res.data)
            .then((data) => {
                setLogs(data);
                console.log("Log List", data);
            })
            .catch((err) => alert(err));
    };

    
    return (
        <div className="projects-section">
            <h2>List of Logs for Game {id}</h2>
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
                {logs.map((log) => (
                    <Link to={`/images/${log.id}`} className="project-box-wrapper" key={log.id}>
                        <LogCard event={log} key={log.name}></LogCard>
                    </Link>
                ))}
            </div>
        </div>


    );
}

export default LogListView;

