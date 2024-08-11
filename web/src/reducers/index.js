import { combineReducers } from 'redux';
import auth from './auth';
import profile from './profile';
import canvasReducer from './canvasSlice';
import breadcrumbReducer from './breadcrumbSlice';
export default combineReducers({
    auth,
    profile,
    canvasReducer,
    breadcrumbReducer
});