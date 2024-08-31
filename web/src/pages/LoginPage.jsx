import LoginForm from "../components/custom/LoginForm";
import "@/styles/login.css"
import logo from "../assets/logo.svg";

const LoginPage = ({ login, isAuthenticated }) => {
  // old: <LoginForm route="/api/token/" method="login" />
  return (
    <div className="container-fluid">
      <div className="left-container">
        <img src={logo} height="93" alt="Berlin United Logo" />
        <div className="credits">
          <p>developed by Stella@Berlin United</p>
        </div>
      </div>
      <div className="right-container">
        <LoginForm route="/api/token/" method="login"/>
      </div>
    </div>
  );
}

export default LoginPage;