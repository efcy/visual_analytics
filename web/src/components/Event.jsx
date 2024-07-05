import React from "react";
import "../styles/new.css"
import "../styles/event.css"
import event_image from'../assets/robocup.jpeg';

function Event({ event }) {
    return (
        <a href="" class="project-box-wrapper">
            <div class="project-box">
                <img src={event_image} alt='' />
                <h3>Card Headline 1</h3>
                <p>Chocolate cake macaroon tootsie roll pastry gummies.</p>
                <p>Apple pie jujubes cheesecake ice cream gummies sweet roll lollipop.</p>
                <a href="https://moderncss.dev">Visit ModernCSS.dev</a>
            </div>
        </a>
    );
}

export default Event