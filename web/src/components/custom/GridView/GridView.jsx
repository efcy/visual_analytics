function GridView({ children }) {
  return (
    <div className="projects-section">
      <div className="project-boxes jsGridView">{children}</div>
    </div>
  );
}

export default GridView;
