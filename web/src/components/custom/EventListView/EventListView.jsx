import "@/styles/new.css";

import { useEvents } from "@/hooks/useEvents";
import EventCard from "../EventCard/EventCard.jsx";
import { useNavigate } from "react-router-dom";
import GridView from "../GridView/GridView.jsx";
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
    <GridView>
      {events.map((event) => (
        <EventCard
          event={event}
          key={event.name}
          event_nav_func={event_nav_func}
        ></EventCard>
      ))}
    </GridView>
  );
}

export default EventListView;
