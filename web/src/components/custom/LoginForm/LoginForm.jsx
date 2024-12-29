import { useState } from "react";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "@/constants";
import classes from "./LoginForm.module.css";
import api from "@/api";
import { useNavigate, Link } from "react-router-dom";

const LoginForm = ({ route, method }) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await api.post(route, { username, password });
      if (method === "login") {
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
        navigate("/");
      } else {
        navigate("/login");
      }
    } catch (error) {
      alert(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={(e) => handleSubmit(e)} className={classes.form_container}>
      <h1>Login</h1>
      <input
        className={classes.form_input}
        type="text"
        name="username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        className={classes.form_input}
        type="password"
        name="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button className={classes.form_button} type="submit">
        Login
      </button>
      <p className={classes.signup_text}>
        Don't have an account?{" "}
        <Link to="/register" className={classes.signup_link}>
          Sign Up
        </Link>
      </p>
    </form>
  );
};

export default LoginForm;
