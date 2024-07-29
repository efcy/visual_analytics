import LoginForm from "../components/custom/LoginForm";
import "@/styles/login.css"
import logo from "../assets/logo.svg";

function LoginPage() {
  return (
    <div className="container-fluid">
      <div className="left-container">
        <img src={logo} height="93" alt="Berlin United Logo" />
        <div className="credits">
          <p>developed by Stella@Berlin United</p>
        </div>
      </div>
      <div className="right-container">
        <LoginForm route="/api/token/" method="login" />
      </div>
    </div>
  );
}

export default LoginPage;
