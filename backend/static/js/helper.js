const isObjectEmpty = (objectName) => {
  // generic function for checking if an javascript object is empty
  // we use it for checking for an empty annotation json
  return (
    objectName &&
    Object.keys(objectName).length === 0 &&
    objectName.constructor === Object
  );
};

const generateUUID4 = () =>{
  // similar to what python would return
  return crypto.randomUUID().replace(/-/g,"").slice(0,9).toUpperCase();
}

const getBoundingBoxTransformer = () => {
  // create new transformer
  var tr = new Konva.Transformer();
  tr.rotateEnabled(false);
  tr.flipEnabled(false);
  tr.anchorStroke("green");
  tr.anchorFill('white');
  tr.keepRatio(false);
  tr.ignoreStroke(true);
  tr.borderStrokeWidth(0);
  tr.enabledAnchors([
      "top-left",
      "top-right",
      "bottom-left",
      "bottom-right",
  ]);
  tr.anchorCornerRadius(10);

  return tr;
};

const scrollTimeline = () => {
  const activeElement = document.querySelector('.timeline-active');
  if (activeElement) {
    activeElement.scrollIntoView({
      behavior: 'smooth', // Smooth scrolling animation
      block: 'nearest',   // Keeps vertical alignment as is (you can adjust if needed)
      inline: 'center',   // Horizontally centers the element in the viewport
    });
  }
};

const arrow_navigation = () => {
  // Get the URLs for the previous and next frames
  const prevLink = document.querySelector('.prev-button');
  const nextLink = document.querySelector('.next-button');

  document.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft' && prevLink && prevLink.href !== '#') {
      // Navigate to the previous frame when the left arrow key is pressed
      window.location.href = prevLink.href;
    } else if (event.key === 'ArrowRight' && nextLink && nextLink.href !== '#') {
      // Navigate to the next frame when the right arrow key is pressed
      window.location.href = nextLink.href;
    }
  });
}