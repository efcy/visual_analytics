// Function to scale images based on constraints
function scaleImages() {
  const mainContent = document.querySelector('.main-content');
  const images = document.querySelectorAll('.image-container img');

  const mainContentWidth = mainContent.clientWidth;
  const mainContentHeight = mainContent.clientHeight;
  console.log(mainContentWidth, mainContentHeight)
  // Constraints
  const maxImageHeight = mainContentHeight / 2 - 20 -40 ; // Half the height of main-content - 2 xpadding - 2 space for caption
  const maxImageWidth = mainContentWidth / 4 -40 ;// One-fourth the width of main-content

  images.forEach((img) => {
    const aspectRatio = img.naturalWidth / img.naturalHeight;

    // Calculate new dimensions based on constraints
    let newWidth = maxImageWidth;
    let newHeight = newWidth / aspectRatio;

    if (newHeight > maxImageHeight) {
      newHeight = maxImageHeight;
      newWidth = newHeight * aspectRatio;
    }

    // Apply new dimensions to the image
    img.style.width = `${newWidth}px`;
    img.style.height = `${newHeight}px`;
  });
}

// Observe changes to the main-content div
const resizeObserver = new ResizeObserver(scaleImages);
const mainContent = document.querySelector('.main-content');
resizeObserver.observe(mainContent);

// Initial scaling
scaleImages();