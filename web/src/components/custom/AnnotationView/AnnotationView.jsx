import { useState, useEffect } from "react";
import api from "@/api";
import { useParams, useNavigate } from "react-router-dom";
import NavigationControls from "../NavigationControls/NavigationControls.jsx";
import DataView from "../DataView/DataView.jsx";
import CanvasView from "../CanvasView/CanvasView.jsx";
import classes from "./AnnotationView.module.css";

const AnnotationView = () => {
  console.log("AnnotationView called");
  const [imageList, setImageList] = useState([]);
  const [frameFilter, setFrameFilter] = useState(0);
  const [currentImage, setCurrentImage] = useState(null);
  const [camera, setCamera] = useState("BOTTOM");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id, imageIndex } = useParams();
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    setIsInitialLoading(true);
    get_image_list();
    console.log("switch camera");
  }, [camera, frameFilter]); // this list is called dependency array

  const get_image_list = () => {
    api
      .get(
        `${import.meta.env.VITE_API_URL}/api/image?log=${id}&camera=${camera}&use_filter=${frameFilter}`,
      )
      .then((res) => res.data)
      .then((data) => {
        setImageList(data);
        setIsInitialLoading(false);

        if (data.length > 0 && (imageIndex < 0 || imageIndex >= data.length)) {
          navigate(`/data/${id}/image/0`, { replace: true });
        }
      })
      .catch((err) => alert(err));
  };

  useEffect(() => {
    if (imageList.length > 0) {
      console.log(imageList);
    }
  }, [imageList]); // this list is called dependency array

  // Load specific image
  const loadImage = (imageIndex) => {
    setIsLoading(true);
    setError(null);

    const currentImageIdx = parseInt(imageIndex);
    if (!imageList[currentImageIdx]) {
      setError("Image not found");
      setIsLoading(false);
      return;
    }

    const imageUrl =
      "https://logs.berlin-united.com/" + imageList[currentImageIdx].image_url;

    return new Promise((resolve, reject) => {
      const img = new Image();

      img.onload = () => {
        setIsLoading(false);
        resolve(img);
      };

      img.onerror = () => {
        setError("Failed to load image");
        setIsLoading(false);
        reject();
      };

      img.src = imageUrl;
      setCurrentImage(img);
    });
  };

  // Load new image when imageIndex changes
  useEffect(() => {
    if (imageList.length > 0) {
      loadImage(imageIndex);
    }
  }, [imageIndex, imageList]);

  return (
    <div className={classes.mainView}>
      <div className={classes.dataView}>
        {currentImage ? (
          <CanvasView
            image={currentImage}
            currentCamera={camera}
            setCamera={setCamera}
            setFrameFilter={setFrameFilter}
          />
        ) : (
          <div>Image not loaded yet</div>
        )}
        <DataView />
      </div>

      <div className="p-4">
        {imageList.length > 0 ? (
          <NavigationControls
            imageIndex={imageIndex}
            totalImages={imageList.length}
            id={id}
          />
        ) : (
          <div></div>
        )}
      </div>
    </div>
  );
};

export default AnnotationView;
