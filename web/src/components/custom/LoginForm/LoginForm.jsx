import { useState } from "react";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "@/constants";
import classes from "./LoginForm.module.css";
import api from "@/api";
import { useNavigate, Link } from "react-router-dom";

const LoginForm = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // TODO why to call the token endpoint here?
      const res = await api.post("/api/token/", { username, password });
      localStorage.setItem(ACCESS_TOKEN, res.data.access);
      localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
      navigate("/");
    } catch (error) {
      alert(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={(e) => handleSubmit(e)} className={classes.form_container}>
      <h1 className={classes.login_header}>Login</h1>
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
        <Link to="/signup" className={classes.signup_link}>
          Sign Up
        </Link>
      </p>
    </form>
  );
};

export default LoginForm;
