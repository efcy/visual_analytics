import classes from "./GridView.module.css";

function GridView({ children }) {
  return (
    <div className={classes.projects_section}>
      <div className={`${classes.project_boxes} ${classes.jsGridView}`}>
        {children}
      </div>
    </div>
  );
}

export default GridView;
