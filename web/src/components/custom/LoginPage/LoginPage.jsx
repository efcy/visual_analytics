import LoginForm from "../LoginForm/LoginForm";
import logo from "@/assets/logo.svg"; // @ is an alias configured in vite.config.ts
import classes from "./LoginPage.module.css";

const LoginPage = ({ login, isAuthenticated }) => {
  return (
    <div className={classes.container_fluid}>
      <div className={classes.left_container}>
        <div className={classes.logo_big}>
          <img src={logo} alt="Berlin United Logo" />
        </div>
        <div className={classes.credits}>
          <p>developed by Berlin United</p>
        </div>
      </div>
      <div className={classes.right_container}>
        <LoginForm route="/api/token/" method="login" />
      </div>
    </div>
  );
};

export default LoginPage;
