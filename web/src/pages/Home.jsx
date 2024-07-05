import { useState, useEffect } from "react";
import "../styles/new.css"
import Event from "../components/Event"
import Header from "../components/header"
import Sidebar from "../components/Sidebar"
import api from "../api";
//import { function1 } from '../js/home.js'

function Home() {
  const [events, setEvents] = useState([]);
  useEffect(() => {
    getEvents();
  }, []);

  const getEvents = () => {
      api
          .get("/api/events/")
          .then((res) => res.data)
          .then((data) => {
              setEvents(data);
              console.log(data);
          })
          .catch((err) => alert(err));
  };

  return (
    <div class="app-container">
      <Header />
      <div class="app-content">
        <Sidebar />
        <div class="projects-section">
          <div class="projects-section-header">
            <p>Projects</p>
            <p class="time">December, 12</p>
          </div>
          <div class="projects-section-line">
            <div class="view-actions">
              <button class="view-btn list-view" title="List View">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-list">
                  <line x1="8" y1="6" x2="21" y2="6" />
                  <line x1="8" y1="12" x2="21" y2="12" />
                  <line x1="8" y1="18" x2="21" y2="18" />
                  <line x1="3" y1="6" x2="3.01" y2="6" />
                  <line x1="3" y1="12" x2="3.01" y2="12" />
                  <line x1="3" y1="18" x2="3.01" y2="18" /></svg>
              </button>
              <button class="view-btn grid-view active" title="Grid View">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-grid">
                  <rect x="3" y="3" width="7" height="7" />
                  <rect x="14" y="3" width="7" height="7" />
                  <rect x="14" y="14" width="7" height="7" />
                  <rect x="3" y="14" width="7" height="7" /></svg>
              </button>
            </div>
          </div>
          <div class="project-boxes jsGridView">
            
            
            {events.map((event) => (
              <Event event={event} key={event.name} />
            ))}
            <Event />
            <Event />
            <Event />
            <Event />
            <Event />
            <Event />
            <Event />
            <Event />
            <Event />
            <Event />
            <Event />
            <Event />
            <Event />
            
          </div>
        </div>
      </div>
    </div>

  );
}

export default Home;