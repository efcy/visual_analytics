import { combineReducers } from 'redux';
import auth from './auth';
import profile from './profile';
import canvasReducer from './canvasSlice';
export default combineReducers({
    auth,
    profile,
    canvasReducer
});