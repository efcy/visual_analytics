import axios from "axios";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "./constants";
import { jwtDecode } from "jwt-decode";
const apiUrl = "http://127.0.0.1:8000/";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || apiUrl,
  withCredentials: false,
  headers: {
    "Content-Type": "application/json",
    Accept: "*/*",
  },
});

const refreshToken = async () => {
  const refreshToken = localStorage.getItem(REFRESH_TOKEN);

  try {
    const baseURL = import.meta.env.VITE_API_URL || apiUrl;
    console.log("base url: ", baseURL);
    const refreshUrl = new URL("api/token/refresh/", api.defaults.baseURL);
    const res = await axios.post(refreshUrl.toString(), {
      refresh: refreshToken,
    });
    if (res.status === 200) {
      localStorage.setItem(ACCESS_TOKEN, res.data.access);
      return res.data.access;
    } else {
      throw new Error("Failed to refresh token");
    }
  } catch (error) {
    console.log("Custom error", error);
    throw error;
  }
};

// Request interceptor
api.interceptors.request.use(
  async (config) => {
    //check for token validity and get a new token if not valid
    let token = localStorage.getItem(ACCESS_TOKEN);
    if (token) {
      const decoded = jwtDecode(token);
      const tokenExpiration = decoded.exp;
      const now = Date.now() / 1000;

      if (tokenExpiration < now) {
        console.log("get new refresh token");
        token = await refreshToken();
      }
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error),
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const newToken = await refreshToken();
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Handle failed refresh (e.g., redirect to login)
        localStorage.removeItem(ACCESS_TOKEN);
        localStorage.removeItem(REFRESH_TOKEN);
        // You might want to use a global state management solution to trigger a redirect
        // For now, we'll just throw an error
        throw new Error("Authentication failed. Please log in again.");
      }
    }
    return Promise.reject(error);
  },
);

export default api;
