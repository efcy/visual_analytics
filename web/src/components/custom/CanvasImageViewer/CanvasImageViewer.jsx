import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { useParams, Link } from "react-router-dom";
import MultiRowRangeSlider from "../MultiRowRangeSlider/MultiRowRangeSlider";
import { useSelector, useDispatch } from "react-redux";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import classes from './CanvasImageViewer.module.css'

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
  const store_idx = useSelector((state) => state.canvasReducer.index);

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

    loadImage(images[store_idx]);
  }, [store_idx, images]);

  useEffect(() => {
    // Preload current image and next few images
    for (let i = 0; i < 5; i++) {
      if (images[store_idx + i]) {
        preloadImage(images[store_idx + i]);
      }
    }
  }, [store_idx, images]);

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
    if (!image_db_obj) {
      return;
    }
    const new_url = 'https://logs.berlin-united.com/' + image_db_obj.image_url
    if (!loadedImages[new_url]) {
      const img = new Image();
      img.src = new_url;
      img.onload = () =>  
        setLoadedImages((prev) => ({ ...prev, [new_url]: img }));
    }
  };

  const loadImage = (image_db_obj) => {
    if (!image_db_obj) {
      return;
    }
    const new_url = 'https://logs.berlin-united.com/' + image_db_obj.image_url
    console.log(new_url);
    //const url = image_db_obj.image_url
    if (loadedImages[new_url]) {
      drawImageOnCanvas(loadedImages[new_url]);
    } else {
      const img = new Image();
      img.onload = () => {
        setLoadedImages((prev) => ({ ...prev, [new_url]: img }));
        drawImageOnCanvas(img);
      };
      img.src = new_url;
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
    boundingBoxes.forEach((box) => {
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
        startPositionRef.current = {
          x: offsetX - clickedBox.startX,
          y: offsetY - clickedBox.startY,
        };
      }
    } else {
      startPositionRef.current = { x: offsetX, y: offsetY };
      setIsDrawing(true);
    }
  };

  const draw = ({ nativeEvent }) => {
    const { offsetX, offsetY } = nativeEvent;
    if (isDrawing) {
      drawBoundingBox(
        startPositionRef.current.x,
        startPositionRef.current.y,
        offsetX,
        offsetY
      );
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
      setBoundingBoxes((prev) => [
        ...prev,
        {
          startX: startPositionRef.current.x,
          startY: startPositionRef.current.y,
          endX: offsetX,
          endY: offsetY,
        },
      ]);
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
    return boundingBoxes.find((box) => {
      const minX = Math.min(box.startX, box.endX) - clickMargin;
      const maxX = Math.max(box.startX, box.endX) + clickMargin;
      const minY = Math.min(box.startY, box.endY) - clickMargin;
      const maxY = Math.max(box.startY, box.endY) + clickMargin;

      return x >= minX && x <= maxX && y >= minY && y <= maxY;
    });
  };

  const getClickedCorner = (box, x, y) => {
    const corners = [
      { x: box.startX, y: box.startY, name: "topLeft" },
      { x: box.endX, y: box.startY, name: "topRight" },
      { x: box.startX, y: box.endY, name: "bottomLeft" },
      { x: box.endX, y: box.endY, name: "bottomRight" },
    ];
    const cornerSize = 10;
    return corners.find(
      (corner) =>
        Math.abs(x - corner.x) < cornerSize &&
        Math.abs(y - corner.y) < cornerSize
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
      case "topLeft":
        box.startX = x;
        box.startY = y;
        break;
      case "topRight":
        box.endX = x;
        box.startY = y;
        break;
      case "bottomLeft":
        box.startX = x;
        box.endY = y;
        break;
      case "bottomRight":
        box.endX = x;
        box.endY = y;
        break;
    }
    redrawCanvas();
  };

  const updateBoxPosition = (box, x, y) => {
    const index = boundingBoxes.findIndex((b) => b === box);
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


  return (
    <div className={classes.mainView}>
      <div className={classes.dataView}>
        <canvas
          className={classes.imageCanvas}
          ref={canvasRef}
          onMouseDown={startDrawing}
          onMouseMove={draw}
          onMouseUp={stopDrawing}
          onMouseLeave={stopDrawing}
        />
        <div className="representationSelector">
          <Accordion type="single" collapsible>
            <AccordionItem value="item-1">
              <AccordionTrigger>Is it accessible?</AccordionTrigger>
              <AccordionContent>
                Yes. It adheres to the WAI-ARIA design pattern.
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </div>
        <div>
          <code>
            asdhoashdohiaosdijoaijsdasosuhdpuasiogdlbaiwhep 
          </code>
        </div>
      </div>

      <div className="p-4">
        <h1 className="text-2xl font-bold mb-4">
          Timeline Example {store_idx}
        </h1>
        <MultiRowRangeSlider />
      </div>
    </div>
  );
};

export default CanvasImageViewer;
