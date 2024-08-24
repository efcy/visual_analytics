import { useState, useEffect, useMemo, useCallback } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import MultiRowRangeSlider from "../MultiRowRangeSlider/MultiRowRangeSlider";
import { useSelector } from "react-redux";
import DataView from "../DataView/DataView.jsx";
import CanvasView from "../CanvasView/CanvasView.jsx";
import classes from "./AnnotationView.module.css";

const AnnotationView = () => {
  const [imageList, setImageList] = useState([]);
  const [preloadedImages, setPreloadedImages] = useState([]);
  const [camera, setCamera] = useState("BOTTOM");
  const { id } = useParams();
  const store_idx = useSelector((state) => state.canvasReducer.index);
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const preloadRange = 10;

  // TODO in the future also preload a few of the other camera images. and then initialize the setPreloadedImages correctly

  useEffect(() => {
    get_image_data();
    setPreloadedImages({});
  }, [camera]); // this list is called dependency array

  const get_image_data = () => {
    axios
      .get(
        `${import.meta.env.VITE_API_URL}/api/image?log=${id}&camera=${camera}`
      )
      .then((res) => res.data)
      .then((data) => {
        setImageList(data);
        console.log("Image List", data);
        setIsInitialLoading(false);
      })
      .catch((err) => alert(err));
  };

  const loadImage = useCallback((url) => {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = url;
    });
  }, []);

  const loadImagesProgressively = useCallback(async () => {
    const startIndex = Math.max(0, store_idx - preloadRange);
    const endIndex = Math.min(imageList.length, store_idx + preloadRange + 1);

    for (let i = startIndex; i < endIndex; i++) {
      if (!preloadedImages[i] && imageList[i]) {
        const imageUrl = "https://logs.berlin-united.com/" + imageList[i].image_url;
        try {
          const loadedImage = await loadImage(imageUrl);
          setPreloadedImages(prev => ({ ...prev, [i]: loadedImage }));
        } catch (error) {
          console.error(`Error loading image at index ${i}:`, error);
        }
      }
    }
  }, [store_idx, imageList, preloadedImages, loadImage, preloadRange, camera]);

  useEffect(() => {
    if (!isInitialLoading) {
      loadImagesProgressively();
    }
  }, [loadImagesProgressively, isInitialLoading]);

  const currentImage = useMemo(() => preloadedImages[store_idx], [preloadedImages, store_idx]);


  return (
    <div className={classes.mainView}>
      <div className={classes.dataView}>
        {currentImage  ? (
        <CanvasView image={currentImage}  setCamera={setCamera}/>
      ) : (
        <div>Image not loaded yet</div>
      )}
        <DataView />
      </div>

      <div className="p-4">
        <MultiRowRangeSlider length={imageList.length} />
      </div>
    </div>
  );
};

export default AnnotationView;
