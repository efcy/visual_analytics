import { useState, useEffect } from "react";
import api from "@/api";
import { useParams, useNavigate  } from "react-router-dom";
import NavigationControls from "../NavigationControls/NavigationControls.jsx";
import DataView from "../DataView/DataView.jsx";
import CanvasView from "../CanvasView/CanvasView.jsx";
import classes from "./AnnotationView.module.css";

const AnnotationView = () => {
  const [frameList, setFrameList] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(null);
  const [frameFilter, setFrameFilter] = useState(0);
  const [currentTopImageData, setCurrentTopImageData] = useState(null);
  const [currentTopImage, setCurrentTopImage] = useState(null);
  const [currentBottomImageData, setCurrentBottomImageData] = useState(null);
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

  useEffect(() => {
    loadImage(currentBottomImageData, setCurrentBottomImage);
  }, [currentBottomImageData]); // this list is called dependency array

  useEffect(() => {
    loadImage(currentTopImageData, setCurrentTopImage);
  }, [currentTopImageData]); // this list is called dependency array

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
      get_image_url(frameNumber)
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

  const get_image_url = ( frameNumber ) => {
    api
      .get(
        `${import.meta.env.VITE_API_URL}/api/image/?log=${id}&camera=BOTTOM&frame_number=${frameNumber}`
      )
      .then((res) => res.data)
      .then((data) => {
        if(data.length > 0){
          setCurrentBottomImageData(data);
        }else{
          setCurrentBottomImageData(null);
          setCurrentBottomImage(null);
        }
      })
      .catch((err) => alert(err));

      api
      .get(
        `${import.meta.env.VITE_API_URL}/api/image/?log=${id}&camera=TOP&frame_number=${frameNumber}`
      )
      .then((res) => res.data)
      .then((data) => {
        if(data.length > 0){
          setCurrentTopImageData(data);
        }else{
          setCurrentTopImageData(null);
          setCurrentTopImage(null);
        }
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

  // Load specific image
  const loadImage = ( current_image_data , set_image ) => {
    setIsLoading(true);
    setError(null);
    if (!current_image_data) {
      setError('Image not found');
      setIsLoading(false);
      return;
    }
    console.log(current_image_data)

    //Fixme build check that list returns only one item
    const imageUrl = "https://logs.berlin-united.com/" + current_image_data[0].image_url;
    console.log(imageUrl)
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
      set_image(img);
    });
  };

  return (
    <div className={classes.mainView}>
      <div className={classes.dataView}>
        {currentTopImage  ? (
        <CanvasView
          image={currentTopImage}
        />
      ) : (
        <div>Image not loaded yet</div>
      )}
      {currentBottomImage  ? (
        <CanvasView
          image={currentBottomImage}
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
