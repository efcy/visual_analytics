import { useState, useEffect, useRef } from "react";
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';
//import Timeline from './Timeline';
import FrameTimeline from './FrameTimeline';
function generateFrameData(baseFrameNumber = 12000, framesCount = 100, intervalSeconds = 5) {
  const frames = [];
  const intervalMs = intervalSeconds * 1000;

  for (let i = 0; i < framesCount; i++) {
    const frameNumber = baseFrameNumber + i;
    const time = i * intervalMs;
    let data = `Frame ${i + 1}`;

    // Check for minute marks
    const minutes = Math.floor(time / 60000);
    if (time % 60000 === 0 && minutes > 0) {
      data = `${minutes} minute mark`;
    }

    frames.push({
      index: i,
      framenumber: frameNumber,
      time: time,
      data: data
    });
  }

  return frames;
}

const CanvasImageViewer = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [images, setImages] = useState([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const [loadedImages, setLoadedImages] = useState({});
  const [boundingBoxes, setBoundingBoxes] = useState([]);
  const [selectedBox, setSelectedBox] = useState(null);
  const [resizingCorner, setResizingCorner] = useState(null);

  const canvasRef = useRef(null);
  const contextRef = useRef(null);
  const { id } = useParams();
  const startPositionRef = useRef({ x: 0, y: 0 });
  const currentImageRef = useRef(null);

  useEffect(() => {
    getImages();
  }, []); // this list is called dependency array

  useEffect(() => {
    const canvas = canvasRef.current;
    canvas.width = 800;
    canvas.height = 600;

    const context = canvas.getContext("2d");
    context.lineCap = "round";
    context.strokeStyle = "red";
    context.lineWidth = 2;
    contextRef.current = context;

    loadImage(images[currentIndex]);
  }, [currentIndex, images]);

  useEffect(() => {
    // Preload current image and next few images
    for (let i = 0; i < 5; i++) {
      if (images[currentIndex + i]) {
        preloadImage(images[currentIndex + i]);
      }
    }
  }, [currentIndex, images]);

  const getImages = () => {
    axios
        .get(`${import.meta.env.VITE_API_URL}/api/image?log=${id}`)
        .then((res) => res.data)
        .then((data) => {
          setImages(data);
            console.log("Image List", data);
        })
        .catch((err) => alert(err));
};

  const preloadImage = (image_db_obj) => {
    if (!image_db_obj){
      return;
    }
    if (!loadedImages[image_db_obj.image_url]) {
      const img = new Image();
      img.src = image_db_obj.image_url;
      img.onload = () => setLoadedImages((prev) => ({ ...prev, [image_db_obj.image_url]: img }));
    }
  };

  const loadImage = (image_db_obj) => {
    if (!image_db_obj){
      return;
    }
    console.log(image_db_obj.image_url)
    //const url = image_db_obj.image_url
    if (loadedImages[image_db_obj.image_url]) {
      drawImageOnCanvas(loadedImages[image_db_obj.image_url]);
    } else {
      const img = new Image();
      img.onload = () => {
        setLoadedImages((prev) => ({ ...prev, [image_db_obj.image_url]: img }));
        drawImageOnCanvas(img);
      };
      img.src = image_db_obj.image_url;
    }
  };

  const drawImageOnCanvas = (img) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Calculate aspect ratio to fit image within canvas
    const scale = Math.min(
      canvas.width / img.width,
      canvas.height / img.height
    );
    const x = canvas.width / 2 - (img.width / 2) * scale;
    const y = canvas.height / 2 - (img.height / 2) * scale;

    ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
    currentImageRef.current = { img, x, y, scale };

    // Redraw existing bounding boxes
    redrawBoundingBoxes();
  };

  const redrawBoundingBoxes = () => {
    boundingBoxes.forEach(box => {
      drawBoundingBox(box.startX, box.startY, box.endX, box.endY, true);
    });
  };

  const startDrawing = ({ nativeEvent }) => {
    const { offsetX, offsetY } = nativeEvent;
    const clickedBox = getClickedBox(offsetX, offsetY);
    console.log("clickedBox: ", clickedBox);
    if (clickedBox) {
      setSelectedBox(clickedBox);
      const corner = getClickedCorner(clickedBox, offsetX, offsetY);
      if (corner) {
        setResizingCorner(corner);
      } else {
        startPositionRef.current = { x: offsetX - clickedBox.startX, y: offsetY - clickedBox.startY };
      }
    } else {
      startPositionRef.current = { x: offsetX, y: offsetY };
      setIsDrawing(true);
    }
  };

  const draw = ({ nativeEvent }) => {
    const { offsetX, offsetY } = nativeEvent;
    if (isDrawing) {
      drawBoundingBox(startPositionRef.current.x, startPositionRef.current.y, offsetX, offsetY);
    } else if (selectedBox) {
      if (resizingCorner) {
        resizeBox(selectedBox, resizingCorner, offsetX, offsetY);
      } else {
        moveBox(selectedBox, offsetX, offsetY);
      }
    }
  };

  const stopDrawing = ({ nativeEvent }) => {
    const { offsetX, offsetY } = nativeEvent;
    if (isDrawing) {
      setBoundingBoxes(prev => [...prev, {
        startX: startPositionRef.current.x,
        startY: startPositionRef.current.y,
        endX: offsetX,
        endY: offsetY
      }]);
      setIsDrawing(false);
    } else if (selectedBox) {
      updateBoxPosition(selectedBox, offsetX, offsetY);
    }
    setSelectedBox(null);
    //setResizingCorner(null);
  };

  const drawBoundingBox = (startX, startY, endX, endY, isRedraw = false) => {
    const ctx = contextRef.current;
    if (!isRedraw) {
      ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      const { img, x, y, scale } = currentImageRef.current;
      ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
      redrawBoundingBoxes();
    }
    
    ctx.beginPath();
    ctx.rect(startX, startY, endX - startX, endY - startY);
    ctx.stroke();
  };

  const getClickedBox = (x, y) => {
    const clickMargin = 5; // Pixels of leeway for clicking near the border
    return boundingBoxes.find(box => {
      const minX = Math.min(box.startX, box.endX) - clickMargin;
      const maxX = Math.max(box.startX, box.endX) + clickMargin;
      const minY = Math.min(box.startY, box.endY) - clickMargin;
      const maxY = Math.max(box.startY, box.endY) + clickMargin;
      
      return x >= minX && x <= maxX && y >= minY && y <= maxY;
    });
  };

  const getClickedCorner = (box, x, y) => {
    const corners = [
      { x: box.startX, y: box.startY, name: 'topLeft' },
      { x: box.endX, y: box.startY, name: 'topRight' },
      { x: box.startX, y: box.endY, name: 'bottomLeft' },
      { x: box.endX, y: box.endY, name: 'bottomRight' }
    ];
    const cornerSize = 10;
    return corners.find(corner => 
      Math.abs(x - corner.x) < cornerSize && Math.abs(y - corner.y) < cornerSize
    )?.name;
  };

  const moveBox = (box, x, y) => {
    const dx = x - startPositionRef.current.x - box.startX;
    const dy = y - startPositionRef.current.y - box.startY;
    box.startX += dx;
    box.startY += dy;
    box.endX += dx;
    box.endY += dy;
    redrawCanvas();
  };

  const resizeBox = (box, corner, x, y) => {
    switch (corner) {
      case 'topLeft':
        box.startX = x;
        box.startY = y;
        break;
      case 'topRight':
        box.endX = x;
        box.startY = y;
        break;
      case 'bottomLeft':
        box.startX = x;
        box.endY = y;
        break;
      case 'bottomRight':
        box.endX = x;
        box.endY = y;
        break;
    }
    redrawCanvas();
  };

  const updateBoxPosition = (box, x, y) => {
    const index = boundingBoxes.findIndex(b => b === box);
    if (index !== -1) {
      const updatedBoxes = [...boundingBoxes];
      updatedBoxes[index] = box;
      setBoundingBoxes(updatedBoxes);
    }
  };

  const redrawCanvas = () => {
    const ctx = contextRef.current;
    ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    const { img, x, y, scale } = currentImageRef.current;
    ctx.drawImage(img, x, y, img.width * scale, img.height * scale);
    redrawBoundingBoxes();
  };
  const goToPrevious = () => {
    setCurrentIndex((prev) => (prev > 0 ? prev - 1 : prev));
    setBoundingBoxes([]);
  };

  const goToNext = () => {
    setCurrentIndex((prev) => (prev < images.length - 1 ? prev + 1 : prev));
    setBoundingBoxes([]);
  };

  const frames = generateFrameData();

  const buttonStyle = {
    padding: "10px 20px",
    fontSize: "16px",
    cursor: "pointer",
    backgroundColor: "#4CAF50",
    color: "white",
    border: "none",
    borderRadius: "5px",
    margin: "0 10px",
  };

  return (
    <div className="projects-section">
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          maxWidth: "800px",
          margin: "0 auto",
        }}
      >
        <canvas
          ref={canvasRef}
          onMouseDown={startDrawing}
          onMouseMove={draw}
          onMouseUp={stopDrawing}
          onMouseLeave={stopDrawing}
          style={{ border: "1px solid #ddd", marginBottom: "20px" }}
        />
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            width: "100%",
            alignItems: "center",
          }}
        >
          <button
            onClick={goToPrevious}
            disabled={currentIndex === 0}
            style={buttonStyle}
          >
            Previous
          </button>
          <span>
            {currentIndex + 1} / {images.length}
          </span>
          <button
            onClick={goToNext}
            disabled={currentIndex === images.length - 1}
            style={buttonStyle}
          >
            Next
          </button>
        </div>
      </div>
      <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Timeline Example</h1>
      <FrameTimeline frames={frames} width={600} />
    </div>
    </div>
  );
};

export default CanvasImageViewer;
