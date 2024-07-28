import { useState, useEffect, useRef } from "react";
import api from "@/api";
import { useParams, Link } from 'react-router-dom';

const CanvasImageViewer = () => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [images, setImages] = useState([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const [loadedImages, setLoadedImages] = useState({});
  const canvasRef = useRef(null);
  const contextRef = useRef(null);
  const { id } = useParams();

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
    api
        .get(`/api/image?log=${id}`)
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
    setCurrentIndex((prev) => (prev > 0 ? prev - 1 : prev));
  };

  const goToNext = () => {
    setCurrentIndex((prev) => (prev < images.length - 1 ? prev + 1 : prev));
  };

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
    </div>
  );
};

export default CanvasImageViewer;
