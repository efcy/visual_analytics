//import LoginForm from "../LoginForm/LoginForm";
import classes from "./RegisterPage.module.css";

const RegisterPage = () => {
  return (
    <div className={classes.background}>
      <div className={classes.form_container}>
        <form>
          <h2>Login</h2>
          <label for="username">Username:</label>
          <input type="text" id="username" name="username" required />

          <label for="password">Password:</label>
          <input type="password" id="password" name="password" required />

          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;
