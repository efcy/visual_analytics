import { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import MultiRowRangeSlider from "../MultiRowRangeSlider/MultiRowRangeSlider";

import { useSelector } from "react-redux";
import DataView from "../DataView/DataView.jsx";
import CanvasView from "../CanvasView/CanvasView.jsx";
import classes from "./AnnotationView.module.css";

const AnnotationView = () => {
  const [images, setImages] = useState([]);
  const [camera, setCamera] = useState("BOTTOM");
  const [loadedImages, setLoadedImages] = useState({});
  const [url, setUrl] = useState("");
  const { id } = useParams();
  const store_idx = useSelector((state) => state.canvasReducer.index);

  useEffect(() => {
    getImages();
  }, [camera]); // this list is called dependency array

  useEffect(() => {
    //loadImage(images[store_idx]);
    if (!images[store_idx]) {
      return;
    }
    const new_url =
      "https://logs.berlin-united.com/" + images[store_idx].image_url;
    console.log("url: ", new_url);
    setUrl(new_url);
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
      .get(
        `${import.meta.env.VITE_API_URL}/api/image?log=${id}&camera=${camera}`
      )
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
    const new_url = "https://logs.berlin-united.com/" + image_db_obj.image_url;
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
    const new_url = "https://logs.berlin-united.com/" + image_db_obj.image_url;
    console.log(new_url);
    //const url = image_db_obj.image_url
    if (loadedImages[new_url]) {
      //drawImageOnCanvas(loadedImages[new_url]);
    } else {
      const img = new Image();
      img.onload = () => {
        setLoadedImages((prev) => ({ ...prev, [new_url]: img }));
        //drawImageOnCanvas(img);
      };
      img.src = new_url;
    }
  };

  return (
    <div className={classes.mainView}>
      <div className={classes.dataView}>
        <CanvasView imageUrl={url} setCamera={setCamera}/>
        <DataView />
      </div>

      <div className="p-4">
        <MultiRowRangeSlider length={images.length} />
      </div>
    </div>
  );
};

export default AnnotationView;
