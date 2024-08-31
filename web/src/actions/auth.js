import Cookies from 'js-cookie';
import axios from 'axios';
import api from "@/api";
import {
    REGISTER_SUCCESS,
    REGISTER_FAIL,
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOGOUT_SUCCESS,
    LOGOUT_FAIL,
    AUTHENTICATED_SUCCESS,
    AUTHENTICATED_FAIL,
    DELETE_USER_SUCCESS,
    DELETE_USER_FAIL
} from './types';

export const checkAuthenticated = () => async dispatch => {
    const config = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    };

    try {
        const res = await api.get(`${import.meta.env.VITE_API_URL}/accounts/authenticated`, config);

        if (res.data.error || res.data.isAuthenticated === 'error') {
            dispatch({
                type: AUTHENTICATED_FAIL,
                payload: false
            });
        }
        else if (res.data.isAuthenticated === 'success') {
            dispatch({
                type: AUTHENTICATED_SUCCESS,
                payload: true
            });
        }
        else {
            dispatch({
                type: AUTHENTICATED_FAIL,
                payload: false
            });
        }
    } catch(err) {
        dispatch({
            type: AUTHENTICATED_FAIL,
            payload: false
        });
    }
};

export const login = (username, password) => async dispatch => {
    const body = JSON.stringify({ username, password });
    try {
        const res = await api.post(`${import.meta.env.VITE_API_URL}/api/token/`, body);

        if (res.data.success) {
            localStorage.setItem('user', JSON.stringify(res.data));
        }

        if (res.data.success) {
            dispatch({
                type: LOGIN_SUCCESS
            });
        } else {
            dispatch({
                type: LOGIN_FAIL
            });
        }
    } catch(err) {
        dispatch({
            type: LOGIN_FAIL
        });
    }
};


export const logout = () => async dispatch => {
    const config = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    };

    const body = JSON.stringify({
        'withCredentials': true
    });

    try {
        const res = await api.post(`${import.meta.env.VITE_API_URL}/accounts/logout`, body, config);

        if (res.data.success) {
            dispatch({
                type: LOGOUT_SUCCESS
            });
        } else {
            dispatch({
                type: LOGOUT_FAIL
            });
        }
    } catch(err) {
        dispatch({
            type: LOGOUT_FAIL
        });
    }
};

export const delete_account = () => async dispatch => {
    const config = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': Cookies.get('csrftoken')
        }
    };

    const body = JSON.stringify({
        'withCredentials': true
    });

    try {
        const res = await api.delete(`${import.meta.env.VITE_API_URL}/accounts/delete`, config, body);

        if (res.data.success) {
            dispatch({
                type: DELETE_USER_SUCCESS
            });
        } else {
            dispatch({
                type: DELETE_USER_FAIL
            });
        }
    } catch (err) {
        dispatch({
            type: DELETE_USER_FAIL
        });
    }
};