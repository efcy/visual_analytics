import React, { useState, useEffect } from "react";
import axios from "axios";

const CSRFToken = () => {
  const [csrftoken, setcsrftoken] = useState("");

  const getCookie = (name) => {
    let cookieValue = null;
    console.log("get cookie");
    if (document.cookie && document.cookie !== "") {
      console.log("found cookie");
      let cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    } else {
      console.log("no cookie :(");
    }
    return cookieValue;
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const config = {
          headers: {
            Accept: "*/*",
            "Content-Type": "application/json",
          },
          withCredentials: true,
        };

        await api.get(
          `${import.meta.env.VITE_API_URL}/accounts/csrf_cookie`,
          config,
        );
        console.log("successfully got crsf token from cookies");
        setcsrftoken(getCookie("csrftoken"));
      } catch (err) {
        console.log(err);
        console.log("failed to get csrf token");
        setcsrftoken("");
      }
    };

    fetchData();
  }, []);

  return <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />;
};

export default CSRFToken;
