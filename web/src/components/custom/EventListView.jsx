import { useState, useEffect } from "react";
import "@/styles/new.css";
import api from "@/api";
import EventCard from "./EventCard/EventCard";
import { useNavigate } from "react-router-dom";

function EventListView() {
  const [events, setEvents] = useState([]);

  const navigate = useNavigate();

  useEffect(() => {
    getEvents();
  }, []); // this list is called dependency array

  const getEvents = () => {
    api
      .get(`${import.meta.env.VITE_API_URL}/api/events`)
      .then((res) => res.data)
      .then((data) => {
        setEvents(data);
      })
      .catch((err) => alert(err));
  };

  const event_nav_func = (event) => {
    navigate(`/events/${event.id}`);
  };

  return (
    <div className="projects-section">
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
