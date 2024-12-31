import { useState, useEffect } from "react";
import "@/styles/new.css";
import api from "@/api";
import EventCard from "./EventCard/EventCard";
import { useNavigate } from "react-router-dom";
import useDebounce from "@/hooks/use_debounce";

function EventListView() {
  const [events, setEvents] = useState([]);
  const [searchtxt, setsearchtxt] = useState([]);

  const debounce = useDebounce(searchtxt, 300);
  const navigate = useNavigate();

  useEffect(() => {
    getEvents();
  }, [debounce]); // this list is called dependency array

  const getEvents = () => {
    api
      .get(`${import.meta.env.VITE_API_URL}/api/events?name=${searchtxt}`)
      .then((res) => res.data)
      .then((data) => {
        setEvents(data);
        console.log("Event List: ", data);
      })
      .catch((err) => alert(err));
  };

  const event_nav_func = (event) => {
    navigate(`/events/${event.id}`);
  };

  return (
    <div className="projects-section">
      <div className="projects-section-line">
        <div className="search-wrapper">
          <input
            className="search-input"
            type="text"
            placeholder="Search"
            value={searchtxt}
            onChange={(e) => setsearchtxt(e.target.value)}
          />
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="20"
            height="20"
            fill="none"
            stroke="currentColor"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            className="feather feather-search"
            viewBox="0 0 24 24"
          >
            <defs></defs>
            <circle cx="11" cy="11" r="8"></circle>
            <path d="M21 21l-4.35-4.35"></path>
          </svg>
        </div>
      </div>
      <div className="project-boxes jsGridView">
        {events.map((event) => (
          <EventCard
            event={event}
            key={event.name}
            event_nav_func={event_nav_func}
          ></EventCard>
        ))}
      </div>
    </div>
  );
}

export default EventListView;
