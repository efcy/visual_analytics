import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    current_event: "",
    current_game: "",
}

export const breadcrumbSlice = createSlice({
    name: 'breadcrumb',
    initialState,
    reducers: {
        set_event: (state, action) => {
            state.current_event = action.payload;
        },
        set_game: (state, action) => {
            state.current_game = action.payload;
        },
        reset_event: (state) => {
            state.current_event = "";
        },
        reset_game: (state) => {
            state.current_game = "";
        },
    }
})

export const { set_event, set_game, reset_event, reset_game } = breadcrumbSlice.actions;
export default breadcrumbSlice.reducer;