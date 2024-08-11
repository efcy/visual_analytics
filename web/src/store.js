import { configureStore } from "@reduxjs/toolkit";
import {thunk} from 'redux-thunk';
import rootReducer from './reducers';
import {
    persistStore,
    persistReducer,
    FLUSH,
    REHYDRATE,
    PAUSE,
    PERSIST,
    PURGE,
    REGISTER,
  } from 'redux-persist';
import storage from 'redux-persist/lib/storage'; // defaults to localStorage for web

const persistConfig = {
    key: 'root',
    storage,
    // Optionally, specify which parts of your state to persist
    whitelist: ['breadcrumb']
  };

const persistedReducer = persistReducer(persistConfig, rootReducer)

export const store = configureStore({
    reducer: persistedReducer,
    middleware: (getDefaultMiddleware) => getDefaultMiddleware({
        serializableCheck: {
            ignoredActions: [FLUSH, REHYDRATE, PAUSE, PERSIST, PURGE, REGISTER],
          },
    }).concat(thunk),
    devTools: process.env.NODE_ENV !== 'production',
});

export const persistor = persistStore(store);