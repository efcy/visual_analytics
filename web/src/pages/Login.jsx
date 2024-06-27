import Form from "../components/Form"
import "../styles/login.css"
import logo from '../assets/logo.svg';

function Login() {
    return (
        <div class="container-fluid">
            <div class="left-container">
                <img src={logo} height="93" 
                alt="Berlin United Logo"
                />
                <div class="credits">
                    <p>developed by Stella@Berlin United</p>
                </div>
            </div>
            <div class="right-container">
                <Form route="/api/token/" method="login" />
            </div>
        </div>
    )
}

export default Login