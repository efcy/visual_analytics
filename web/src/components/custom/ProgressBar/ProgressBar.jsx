import React from "react";
import classes from "./ProgressBar.module.css";

export const ProgressBar = ({ value, maxValue = 100 }) => (
  <progress className={classes.progress_bar} value={value} max={maxValue}>
    {value}%
  </progress>
);
