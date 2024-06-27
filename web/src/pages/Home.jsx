import { useState, useEffect } from "react";
import "../styles/new.css"


function Home() {
  return (
    <div class="app-container">
      <div class="app-header">
        <div class="app-header-left">
          <span class="app-icon"></span>
          <p class="app-name">Portfolio</p>
          <div class="search-wrapper">
            <input class="search-input" type="text" placeholder="Search" />
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="feather feather-search" viewBox="0 0 24 24">
              <defs></defs>
              <circle cx="11" cy="11" r="8"></circle>
              <path d="M21 21l-4.35-4.35"></path>
            </svg>
          </div>
        </div>
        <div class="app-header-right">
          <button class="mode-switch" title="Switch Theme">
            <svg class="moon" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" width="24" height="24" viewBox="0 0 24 24">
              <defs></defs>
              <path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"></path>
            </svg>
          </button>
          <button class="add-btn" title="Add New Project">
            <svg class="btn-icon" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" class="feather feather-plus">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" /></svg>
          </button>
          <button class="notification-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-bell">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
              <path d="M13.73 21a2 2 0 0 1-3.46 0" /></svg>
          </button>
          <button class="profile-btn">
            <img src="https://assets.codepen.io/3306515/IMG_2025.jpg" />
            <span>Aybüke C.</span>
          </button>
        </div>
      </div>
      <div class="app-content">
        <div class="app-sidebar">
          <a href="" class="app-sidebar-link active">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-home">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
              <polyline points="9 22 9 12 15 12 15 22" /></svg>
          </a>
          <a href="" class="app-sidebar-link">
            <svg class="link-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="feather feather-pie-chart" viewBox="0 0 24 24">
              <defs />
              <path d="M21.21 15.89A10 10 0 118 2.83M22 12A10 10 0 0012 2v10z" />
            </svg>
          </a>
          <a href="" class="app-sidebar-link">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-calendar">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
              <line x1="16" y1="2" x2="16" y2="6" />
              <line x1="8" y1="2" x2="8" y2="6" />
              <line x1="3" y1="10" x2="21" y2="10" /></svg>
          </a>
          <a href="" class="app-sidebar-link">
            <svg class="link-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" class="feather feather-settings" viewBox="0 0 24 24">
              <defs />
              <circle cx="12" cy="12" r="3" />
              <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z" />
            </svg>
          </a>
        </div>
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
                  <p class="box-content-header">Web Designing</p>
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
                  <p class="box-content-header">Web Designing</p>
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
                  <p class="box-content-header">Web Designing</p>
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
                  <p class="box-content-header">Web Designing</p>
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
                  <p class="box-content-header">Web Designing</p>
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
                  <p class="box-content-header">Web Designing</p>
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
                  <p class="box-content-header">Web Designing</p>
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
                  <p class="box-content-header">Web Designing</p>
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
                  <p class="box-content-header">Web Designing</p>
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
                  <p class="box-content-header">Web Designing</p>
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
                  <p class="box-content-header">Web Designing</p>
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
                  <p class="box-content-header">Web Designing</p>
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
                  <p class="box-content-header">Web Designing</p>
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
          </div>
        </div>
      </div>
    </div>

  );
}

export default Home;