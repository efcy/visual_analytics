import { useState, useEffect, useDebugValue } from "react";
import api from "@/api";

export const useLogs = (id) => {
  const [logs, setLogs] = useState(null);
  useDebugValue(logs ? `${logs}` : "Loading...");
  useEffect(() => {
    async function fetchLogs() {
      api
        .get(`${import.meta.env.VITE_API_URL}/api/logs?game_id=${id}`)
        .then((res) => res.data)
        .then((data) => {
          setLogs(data);
        })
        .catch((err) => alert(err));
    }

    fetchLogs();
  }, []);

  return logs;
};

export const useLog = (id) => {
  const [log, setLog] = useState(null);
  useDebugValue(log ? `${log}` : "Loading...");
  useEffect(() => {
    async function fetchLogs() {
      api
        .get(`${import.meta.env.VITE_API_URL}/api/logs/${id}`)
        .then((res) => res.data)
        .then((data) => {
          setLog(data);
        })
        .catch((err) => alert(err));
    }

    fetchLogs();
  }, []);

  return log;
};
