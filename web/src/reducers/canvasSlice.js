import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    index: 0
}

export const canvasSlice = createSlice({
    name: 'canvas',
    initialState,
    reducers: {
        set: (state, action) => {
            state.index = action.payload;
        } 
    }
})

export const { set } = canvasSlice.actions;
export default canvasSlice.reducer;