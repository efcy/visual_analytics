import LoginForm from "../../components/custom/LoginForm/LoginForm";
import logo from "../../assets/logo.svg";
import classes from "./LoginPage.module.css";

const LoginPage = ({ login, isAuthenticated }) => {
  return (
    <div className={classes.container_fluid}>
      <div className={classes.left_container}>
        <img src={logo} height="93" alt="Berlin United Logo" />
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
