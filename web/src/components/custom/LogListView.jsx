import { useState, useEffect } from "react";
import "@/styles/new.css";
import { useParams, Link } from "react-router-dom";
import LogCard from "./LogCard/LogCard";
import api from "@/api";

function LogListView() {
  const [logs, setLogs] = useState([]);
  const { id } = useParams();
  useEffect(() => {
    getLogs();
  }, []); // this list is called dependency array

  const getLogs = () => {
    api
      .get(`${import.meta.env.VITE_API_URL}/api/logs?game_id=${id}`)
      .then((res) => res.data)
      .then((data) => {
        setLogs(data);
        console.log("Log List", data);
      })
      .catch((err) => alert(err));
  };

  return (
    <div className="projects-section">
      <div className="project-boxes jsGridView">
        {logs.map((log) => (
          <Link
            to={`/data/${log.id}`}
            className="project-box-wrapper"
            key={log.id}
          >
            <LogCard log={log} key={log.name}></LogCard>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default LogListView;
