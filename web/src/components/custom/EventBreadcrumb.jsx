import React, { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import axios from 'axios';
import Cookies from 'js-cookie';
import {
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
  } from "@/components/ui/breadcrumb"
import "@/styles/new.css";
import api from "@/api";

const useEventData = (id) => {
    const [eventName, setEventName] = useState('');
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);
  
    useEffect(() => {
      const fetchEventData = async () => {
        setIsLoading(true);
        try {
            const config = {
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    'X-CSRFToken': Cookies.get('csrftoken')
                },
                params: { id }
            };
          const response = await axios.get(`${import.meta.env.VITE_API_URL}/api/events`, config);
          setEventName(response.data.name);
          setError(null);
          console.log(response) 
        } catch (err) {
          console.error('Error fetching event data:', err);
          setError(err.response?.data?.message || 'Failed to load event data');
          setEventName('Unknown Event');
        } finally {
          setIsLoading(false);
          
        }
      };
  
      fetchEventData();
    }, [id]);
  
    return { eventName, isLoading, error };
  };

  const EventBreadcrumb = () => {
    const { id } = useParams();
    const { eventName, isLoading, error } = useEventData(id);
    console.log("eventName", eventName)
    return (
    
      <Breadcrumb className="ps-8">
      <BreadcrumbList>
        <BreadcrumbItem className="text-xl">
          <BreadcrumbLink asChild>
            <Link to="/">Events</Link>
          </BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbSeparator className="text-xl" />
        <BreadcrumbItem className="text-xl">
          <BreadcrumbLink>
            {isLoading ? 'Loading...' : error ? error : eventName}
          </BreadcrumbLink>
        </BreadcrumbItem>
        </BreadcrumbList>
      </Breadcrumb>
      
    );
  };

export default EventBreadcrumb;
