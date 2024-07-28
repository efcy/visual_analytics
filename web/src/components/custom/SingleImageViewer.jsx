import React, { useState, useEffect } from 'react';

const SingleImageViewer = ({ imageUrls }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loadedImages, setLoadedImages] = useState({});

  const preloadImage = (url) => {
    if (!loadedImages[url]) {
      const img = new Image();
      img.src = url;
      img.onload = () => setLoadedImages(prev => ({ ...prev, [url]: true }));
    }
  };

  useEffect(() => {
    // Preload current image and next few images
    for (let i = 0; i < 5; i++) {
      if (imageUrls[currentIndex + i]) {
        preloadImage(imageUrls[currentIndex + i]);
      }
    }
  }, [currentIndex, imageUrls]);

  const goToPrevious = () => {
    setCurrentIndex(prev => (prev > 0 ? prev - 1 : prev));
  };

  const goToNext = () => {
    setCurrentIndex(prev => (prev < imageUrls.length - 1 ? prev + 1 : prev));
  };

  const buttonStyle = {
    padding: '10px 20px',
    fontSize: '16px',
    cursor: 'pointer',
    backgroundColor: '#4CAF50',
    color: 'white',
    border: 'none',
    borderRadius: '5px',
    margin: '0 10px'
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ width: '100%', height: '500px', display: 'flex', justifyContent: 'center', alignItems: 'center', border: '1px solid #ddd', marginBottom: '20px' }}>
        {loadedImages[imageUrls[currentIndex]] ? (
          <img 
            src={imageUrls[currentIndex]} 
            alt={`Image ${currentIndex + 1}`} 
            style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
          />
        ) : (
          <div>Loading...</div>
        )}
      </div>
      <div style={{ display: 'flex', justifyContent: 'space-between', width: '100%', alignItems: 'center' }}>
        <button onClick={goToPrevious} disabled={currentIndex === 0} style={buttonStyle}>
          Previous
        </button>
        <span>{currentIndex + 1} / {imageUrls.length}</span>
        <button onClick={goToNext} disabled={currentIndex === imageUrls.length - 1} style={buttonStyle}>
          Next
        </button>
      </div>
    </div>
  );
};

export default SingleImageViewer;