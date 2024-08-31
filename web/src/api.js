import axios from "axios";
import { ACCESS_TOKEN } from "./constants";

const apiUrl = "http://127.0.0.1:8000/";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : apiUrl,
  withCredentials: false,
  headers: {
    'Content-Type': 'application/json',
    'Accept': '*/*',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('user');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;