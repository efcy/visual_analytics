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
  const [images, setImages] = useState([]);
  const [loadedImages, setLoadedImages] = useState({});

  const canvasRef = useRef(null);
  const contextRef = useRef(null);
  const { id } = useParams();
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
  };

  return (
    <div className={classes.mainView}>
      <div className={classes.dataView}>
        <canvas
          className={classes.imageCanvas}
          ref={canvasRef}
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
        <MultiRowRangeSlider length={images.length}/>
      </div>
    </div>
  );
};

export default CanvasImageViewer;
