import { useState } from "react";
import classes from "./RegisterPage.module.css";
import { useNavigate, Link } from "react-router-dom";
import api from "@/api";

// https://www.youtube.com/watch?v=fn6RH9qVP9w&ab_channel=CodeWithClinton
// Maybe use react hook form for frontend validation

const RegisterPage = () => {
  const [username, setUsername] = useState("asd");
  const [email, setEmail] = useState("bbbbbbbbb");
  const [password, setPassword] = useState("aaaa");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Send a POST request to the backend with the user's email and password
    const user = {
      email: email,
      password: password,
    };
    try {
      const res = await api.post("/accounts/register", user);
      navigate("/");
    } catch (error) {
      alert(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={classes.background}>
      <div className={classes.form_container}>
        <form onSubmit={(e) => handleSubmit(e)}>
          <h2>Sign Up</h2>
          <input
            className={classes.form_input}
            type="text"
            id="email"
            name="email"
            placeholder="Email"
            required
          />
          <input
            className={classes.form_input}
            type="password"
            id="password"
            name="password"
            placeholder="Password"
            required
          />
          <input
            className={classes.form_input}
            type="password"
            id="password_confirm"
            name="confirmPassword"
            placeholder="Confirm password"
            required
          />

          <button className={classes.form_button} type="submit">
            Submit
          </button>
          <p className={classes.signup_text}>
            Already have an account?{" "}
            <Link to="/login" className={classes.login_link}>
              Login
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;
