function calculateAndDisplayDivs(containerId) {
  const container = document.getElementById(containerId);

  // Ensure the container exists
  if (!container) {
    console.error(`Container with ID ${containerId} not found.`);
    return;
  }

  // Get container dimensions
  const containerWidth = container.offsetWidth;
  const containerHeight = container.offsetHeight;

  // Define the size range for divs
  const maxWidth = 640,
    maxHeight = 480;
  const minWidth = 320,
    minHeight = 240;

  let divWidth = maxWidth;
  let divHeight = maxHeight;

  // Find the largest size that fits within the container
  while (divWidth >= minWidth && divHeight >= minHeight) {
    const cols = Math.floor(containerWidth / divWidth);
    const rows = Math.floor(containerHeight / divHeight);

    if (cols * rows > 0) break; // If at least one div fits, stop reducing size

    divWidth -= 10;
    divHeight = divWidth * (3 / 4); // Maintain the 4:3 aspect ratio
  }

  // Clear the container before populating
  container.innerHTML = "";

  // Create the divs and arrange them in the grid
  const cols = Math.floor(containerWidth / divWidth);
  const rows = Math.floor(containerHeight / divHeight);
  const totalDivs = cols * rows;

  for (let i = 0; i < totalDivs; i++) {
    const div = document.createElement("div");
    div.style.width = `${divWidth}px`;
    div.style.height = `${divHeight}px`;
    div.style.border = "1px solid black";
    div.style.boxSizing = "border-box";
    div.style.display = "inline-block";
    container.appendChild(div);
  }
}

// Example usage: Pass the ID of the container element
calculateAndDisplayDivs("container");
