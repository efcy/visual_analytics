import { useState, useEffect } from "react";
import api from "@/api";
import { useParams, useNavigate  } from "react-router-dom";
import NavigationControls from "../NavigationControls/NavigationControls.jsx";
import useImageLoader from "./useImageLoader.jsx";
import DataView from "../DataView/DataView.jsx";
import CanvasView from "../CanvasView/CanvasView.jsx";
import classes from "./AnnotationView.module.css";

const AnnotationView = () => {
  const [frameList, setFrameList] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(null);
  const [frameFilter, setFrameFilter] = useState(0);
  const [camera, setCamera] = useState("BOTTOM");
  const { id, frameNumber  } = useParams();

  useEffect(() => {
    get_frame_list();
  }, [camera, frameFilter]); // this list is called dependency array

  useEffect(() => {
    console.log("frameList.length", frameList.length)
  }, [frameList]); // this list is called dependency array

  // Load new image when imageIndex changes
  useEffect(() => {
    if (frameList.length > 0) {
      // Convert current frame number to number for comparison
      const currentFrame = parseInt(frameNumber);

      const currentIndex = frameList.findIndex(
        frame => frame.frame_number === currentFrame
      );
      setCurrentIndex(currentIndex)
    }
  }, [frameNumber, frameList]);

  const get_frame_list = () => {
    api
      .get(
        `${import.meta.env.VITE_API_URL}/api/cognitionrepr/?log_id=${id}&representation_name=FrameInfo&use_filter=${frameFilter}`
      )
      .then((res) => res.data)
      .then((data) => {
        setFrameList(data);
      })
      .catch((err) => alert(err));
  };

  /*
  const get_annotations = () => {
    const currentImageIdx = parseInt(imageIndex);
    if (!imageList[currentImageIdx]) {
      setError('Image not found');
      setIsLoading(false);
      return;
    }
    //3389974
    api
      .get(
        `${import.meta.env.VITE_API_URL}/api/annotation/3389974`
        //`${import.meta.env.VITE_API_URL}/api/annotation/${imageList[currentImageIdx].id}`
      )
      .then((res) => res.data)
      .then((data) => {
        
        setcurrentAnnotations(data);
      })
      .catch((err) => {
        if (error.response.status === 404){
          setcurrentAnnotations(null);
        }
        else{
          alert(err)
        }
      });
    
  };
  */
  const { topImage, bottomImage, isLoading, error, reloadImages } = useImageLoader(id, frameNumber, api);

  return (
    <div className={classes.mainView}>
      <div className={classes.dataView}>
        {!isLoading  ? (
        <CanvasView
          image={topImage}
        />
      ) : (
        <div>Image not loaded yet</div>
      )}
      {!isLoading  ? (
        <CanvasView
          image={bottomImage}
        />
      ) : (
        <div>Image not loaded yet</div>
      )}
        <DataView />
      </div>
       
      <div className="p-4">
      {frameList.length > 0  ? (
        <NavigationControls
          frameList={frameList}
          frameIndex={currentIndex}
          totalFrames={frameList.length}
          id={id}
          setFrameFilter={setFrameFilter}
          currentCamera={camera}
          setCamera={setCamera}
        />
      ) : (
        <div></div>
      )}
      </div>
    </div>
  );
};

export default AnnotationView;
