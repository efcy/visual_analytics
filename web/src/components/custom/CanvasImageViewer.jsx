import { useState, useEffect, useRef } from 'react';

const CanvasImageViewer = ({ imageUrls }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isDrawing, setIsDrawing] = useState(false);
  const [loadedImages, setLoadedImages] = useState({});
  const canvasRef = useRef(null);
  const contextRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    canvas.width = 800;
    canvas.height = 600;
    
    const context = canvas.getContext('2d');
    context.lineCap = 'round';
    context.strokeStyle = 'red';
    context.lineWidth = 2;
    contextRef.current = context;

    loadImage(imageUrls[currentIndex]);
  }, [currentIndex, imageUrls]);

  useEffect(() => {
    // Preload current image and next few images
    for (let i = 0; i < 5; i++) {
      if (imageUrls[currentIndex + i]) {
        preloadImage(imageUrls[currentIndex + i]);
      }
    }
  }, [currentIndex, imageUrls]);

  const preloadImage = (url) => {
    if (!loadedImages[url]) {
      const img = new Image();
      img.src = url;
      img.onload = () => setLoadedImages(prev => ({ ...prev, [url]: img }));
    }
  };

  const loadImage = (url) => {
    if (loadedImages[url]) {
      drawImageOnCanvas(loadedImages[url]);
    } else {
      const img = new Image();
      img.onload = () => {
        setLoadedImages(prev => ({ ...prev, [url]: img }));
        drawImageOnCanvas(img);
      };
      img.src = url;
    }
  };

  const drawImageOnCanvas = (img) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Calculate aspect ratio to fit image within canvas
    const scale = Math.min(canvas.width / img.width, canvas.height / img.height);
    const x = (canvas.width / 2) - (img.width / 2) * scale;
    const y = (canvas.height / 2) - (img.height / 2) * scale;
    
    ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
  };

  const startDrawing = ({ nativeEvent }) => {
    const { offsetX, offsetY } = nativeEvent;
    contextRef.current.beginPath();
    contextRef.current.moveTo(offsetX, offsetY);
    setIsDrawing(true);
  };

  const draw = ({ nativeEvent }) => {
    if (!isDrawing) return;
    const { offsetX, offsetY } = nativeEvent;
    contextRef.current.lineTo(offsetX, offsetY);
    contextRef.current.stroke();
  };

  const stopDrawing = () => {
    contextRef.current.closePath();
    setIsDrawing(false);
  };

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
      <canvas
        ref={canvasRef}
        onMouseDown={startDrawing}
        onMouseMove={draw}
        onMouseUp={stopDrawing}
        onMouseLeave={stopDrawing}
        style={{ border: '1px solid #ddd', marginBottom: '20px' }}
      />
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

export default CanvasImageViewer;