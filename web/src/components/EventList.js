import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EventList = () => {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        axios.get('/api/events/')
            .then(response => {
                setEvents(response.data);
            })
            .catch(error => {
                console.error("There was an error fetching the events!", error);
            });
    }, []);

    return (
        <div>
            <h1>Event List</h1>
            <ul>
                {events.map(event => (
                    <li key={event.id}>{event.title}</li>
                ))}
            </ul>
        </div>
    );
};

export default EventList;