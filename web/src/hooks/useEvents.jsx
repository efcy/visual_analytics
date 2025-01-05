import { useState, useEffect, useDebugValue } from "react";
import api from "@/api";

export const useEvents = () => {
  const [events, setEvents] = useState(null);
  useDebugValue(events ? `${events}` : "Loading...");
  useEffect(() => {
    async function fetchEvents() {
      api
        .get(`${import.meta.env.VITE_API_URL}/api/events`)
        .then((res) => res.data)
        .then((data) => {
          setEvents(data);
        })
        .catch((err) => alert(err));
    }

    fetchEvents();
  }, []);

  return events;
};
