import { useState, useEffect, useMemo, useCallback } from "react";
import api from "@/api";
import { useParams } from "react-router-dom";
import MultiRowRangeSlider from "../MultiRowRangeSlider/MultiRowRangeSlider";
import { useSelector } from "react-redux";
import DataView from "../DataView/DataView.jsx";
import CanvasView from "../CanvasView/CanvasView.jsx";
import classes from "./AnnotationView.module.css";

const AnnotationView = () => {
  console.log("AnnotationView called")
  const [imageList, setImageList] = useState([]);
  const [preloadedImagesBottom, setPreloadedImagesBottom] = useState([]);
  const [preloadedImagesTop, setPreloadedImagesTop] = useState([]);
  const [camera, setCamera] = useState("BOTTOM");
  const { id } = useParams();
  const store_idx = useSelector((state) => state.canvasReducer.index);
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const preloadRange = 4;

  // TODO in the future also preload a few of the other camera images. and then initialize the setPreloadedImages correctly

  useEffect(() => {
    setIsInitialLoading(true);
    get_image_list();
    setPreloadedImagesBottom([]);
    setPreloadedImagesTop([]);
    console.log("switch camera")
  }, [camera]); // this list is called dependency array

  const get_image_list = () => {
    api
      .get(
        `${import.meta.env.VITE_API_URL}/api/image?log=${id}&camera=${camera}&use_filter=1`
      )
      .then((res) => res.data)
      .then((data) => {
        setImageList(data);
        setIsInitialLoading(false);
      })
      .catch((err) => alert(err));
  };

  useEffect(() => {
    if(imageList.length > 0){
      console.log(imageList[0])
    }
    
  }, [imageList]); // this list is called dependency array
  
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
    const endIndex = Math.min(imageList.length - 1, store_idx + preloadRange + 1);
    var updatedArray = [];
    var preloaded_images = Object()

    if (camera === "TOP"){
      preloaded_images = preloadedImagesTop
      updatedArray = [...preloadedImagesTop];
    }else{
      preloaded_images = preloadedImagesBottom
      updatedArray = [...preloadedImagesBottom];
    }

    for (let i = startIndex; i < endIndex; i++) {
      if (!preloaded_images[i] && imageList[i]) {
        const imageUrl = "https://logs.berlin-united.com/" + imageList[i].image_url;
        try {
          const loadedImage = await loadImage(imageUrl);
          // copy existing array => research better ways
          // one idea is to not have it in state
          updatedArray[i] = loadedImage;
        } catch (error) {
          console.error(`Error loading image at index ${i}:`, error);
        }
      }
    }
    // delete previous entries
    for (let i = 0; i < startIndex; i++) {
      updatedArray[i] = null;
    }
    // delete images after the range
    for (let i = endIndex; i < imageList.length - 1; i++) {
      updatedArray[i] = null;
    }

    // set state
    if (camera === "TOP"){
      setPreloadedImagesTop(updatedArray);
    }else{
      setPreloadedImagesBottom(updatedArray);
    }

  }, [store_idx, imageList, loadImage, preloadRange, camera]);

  useEffect(() => {
    if (!isInitialLoading) {
      loadImagesProgressively();
    }
  }, [loadImagesProgressively, isInitialLoading]);
  /*
  useEffect(() => {
    console.log(preloadedImages)
  }, [preloadedImages]); // this list is called dependency array
  */

  // FIXME
  const currentImage = useMemo(() => {
    if (camera === "TOP"){
      return preloadedImagesTop[store_idx];
    }else{
      return preloadedImagesBottom[store_idx];
    }
    
  },
  [preloadedImagesBottom, preloadedImagesTop, store_idx, camera]);


  return (
    <div className={classes.mainView}>
      <div className={classes.dataView}>
        {currentImage  ? (
        <CanvasView image={currentImage}  currentCamera={camera} setCamera={setCamera}/>
      ) : (
        <div>Image not loaded yet</div>
      )}
        <DataView />
      </div>

      <div className="p-4">
      {imageList.length > 0  ? (
        <MultiRowRangeSlider length={imageList.length} />
      ) : (
        <div></div>
      )}
      </div>
    </div>
  );
};

export default AnnotationView;
