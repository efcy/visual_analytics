//import LoginForm from "../LoginForm/LoginForm";
import classes from "./RegisterPage.module.css";
import { useNavigate, Link } from "react-router-dom";

const RegisterPage = () => {
  return (
    <div className={classes.background}>
      <div className={classes.form_container}>
        <form>
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
            id="password"
            name="confirmPassword"
            placeholder="Confirm password"
            required
          />

          <button className={classes.form_button} type="submit">
            Submit
          </button>
          <p className={classes.signup_text}>
            Already have an account?{" "}
            <Link to="/signup" className={classes.login_link}>
              Login
            </Link>
          </p>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;
