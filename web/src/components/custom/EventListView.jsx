import "@/styles/new.css";

import { useEvents } from "@/hooks/useEvents";
import EventCard from "./EventCard/EventCard";
import { useNavigate } from "react-router-dom";

function EventListView() {
  const navigate = useNavigate();
  const events = useEvents();

  if (!events) {
    return <div>Loading...</div>;
  }

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
