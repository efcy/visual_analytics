import { useState, useEffect } from "react";
import api from "@/api";
import { useParams, useNavigate  } from "react-router-dom";
import NavigationControls from "../NavigationControls/NavigationControls.jsx";
import DataView from "../DataView/DataView.jsx";
import CanvasView from "../CanvasView/CanvasView.jsx";
import classes from "./AnnotationView.module.css";

const AnnotationView = () => {
  console.log("AnnotationView called")
  const [frameList, setFrameList] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(null);
  const [frameFilter, setFrameFilter] = useState(0);
  const [currentTopImage, setCurrentTopImage] = useState(null);
  const [currentBottomImage, setCurrentBottomImage] = useState(null);
  const [currentAnnotations, setcurrentAnnotations] = useState(null);
  const [camera, setCamera] = useState("BOTTOM");
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const { id, frameNumber  } = useParams();
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const navigate = useNavigate();


  useEffect(() => {
    setIsInitialLoading(true);
    get_frame_list();
    setIsInitialLoading(false);
  }, [camera, frameFilter]); // this list is called dependency array

  //useEffect(() => {
  //  get_annotations();
  //}, [imageIndex, imageList]); // this list is called dependency array

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
      console.log("frameList[10]", frameList[10])
      console.log("frameNumber", frameNumber)
      console.log("currentFrame", currentFrame)
      console.log("currentIndex", currentIndex)
      //getImageId(frameidx);
    }
  }, [frameNumber, frameList]);

  const get_frame_list = () => {
    api
      .get(
        `${import.meta.env.VITE_API_URL}/api/cognitionrepr/?log_id=168&representation_name=FrameInfo&use_filter=${frameFilter}`
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
  /*
  const getImageId = ( frameidx ) => {
    const currentFrameidx= parseInt(frameidx);
    if (!frameList[currentFrameidx]) {
      setError('frame not found');
      setIsLoading(false);
      return;
    }
    api
      .get(
        `${import.meta.env.VITE_API_URL}/api/image/?log=${id}&frame_number=${frameFilter}`
      )
      .then((res) => res.data)
      .then((data) => {
        setFrameList(data);
      })
      .catch((err) => alert(err));
  };
  }
  */
  // Load specific image
  /*
  const loadImage = ( frameidx ) => {
    setIsLoading(true);
    setError(null);

    const currentFrameidx= parseInt(frameidx);
    if (!imageList[currentImageIdx]) {
      setError('Image not found');
      setIsLoading(false);
      return;
    }

    lookup = {
      image_id: idx,

    }
    lookup.value() == 2

    const imageUrl = "https://logs.berlin-united.com/" + imageList[currentImageIdx].image_url;
    
    return new Promise((resolve, reject) => {
      const img = new Image();
      
      img.onload = () => {
        setIsLoading(false);
        resolve(img);
      };
      
      img.onerror = () => {
        setError('Failed to load image');
        setIsLoading(false);
        reject();
      };

      img.src = imageUrl;
      setCurrentImage(img);
    });
  };
   */
  return (
    <div className={classes.mainView}>
      <div className={classes.dataView}>
        {currentTopImage  ? (
        <CanvasView
          image={currentTopImage}
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
      {frameList.length > 0  ? (
        <NavigationControls
          frameList={frameList}
          frameIndex={currentIndex}
          totalFrames={frameList.length}
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
