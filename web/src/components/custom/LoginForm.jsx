import { useState, useEffect } from "react";
import { connect } from 'react-redux';
import { login } from '@/actions/auth';
import CSRFToken from './CSRFToken';
import "@/styles/login.css"
import { useNavigate } from "react-router-dom";


const LoginForm = ({ login, isAuthenticated }) => {

    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });

    const { username, password } = formData;
    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = e => {
        e.preventDefault();
        console.log(username)
        login(username, password);
    };
    const navigate = useNavigate();

    useEffect(() => {
        if (isAuthenticated) {
            navigate('/');
        }
    }, [isAuthenticated, navigate]);

    return (
        <form onSubmit={e => onSubmit(e)} className="form-container">
            <CSRFToken />
            <h1>Login</h1>
            <input
                className="form-input"
                type="text"
                name='username'
                value={username}
                onChange={e => onChange(e)}
                placeholder="Username"
            />
            <input
                className="form-input"
                type="password"
                name='password' 
                value={password}
                onChange={e => onChange(e)}
                placeholder="Password"
            />
            
            <button className="form-button" type="submit">
                Login
            </button>
        </form>
    );
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
  });

export default connect(mapStateToProps, { login })(LoginForm);