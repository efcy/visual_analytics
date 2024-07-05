import React from "react";
import "../styles/new.css"


function Event({ event }) {
    //const formattedDate = new Date(note.created_at).toLocaleDateString("en-US")

    return (
        <div class="project-box-wrapper">
            <div class="project-box">
                <div class="project-box-header">
                    <span>December 10, 2020</span>
                    <div class="more-wrapper">
                        <button class="project-btn-more">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-more-vertical">
                                <circle cx="12" cy="12" r="1" />
                                <circle cx="12" cy="5" r="1" />
                                <circle cx="12" cy="19" r="1" /></svg>
                        </button>
                    </div>
                </div>
                <div class="project-box-content-header">
                    <p class="box-content-header">{event ? event.name: "blabla"}</p>
                    <p class="box-content-subheader">Prototyping</p>
                </div>
                <div class="box-progress-wrapper">
                    <p class="box-progress-header">Progress</p>
                    <div class="box-progress-bar">
                        <span class="box-progress"></span>
                    </div>
                    <p class="box-progress-percentage">60%</p>
                </div>
                <div class="project-box-footer">
                    <div class="participants">
                        <button class="add-participant" >
                            <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="feather feather-plus">
                                <path d="M12 5v14M5 12h14" />
                            </svg>
                        </button>
                    </div>
                    <div class="days-left">
                        2 Days Left
                    </div>
                </div>
            </div>
        </div>
    );
}

export default Event