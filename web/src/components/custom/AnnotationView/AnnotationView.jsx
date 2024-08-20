import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { useParams, Link } from "react-router-dom";
import MultiRowRangeSlider from "../MultiRowRangeSlider/MultiRowRangeSlider";
import { useSelector, useDispatch } from "react-redux";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import CanvasView from "../CanvasView.jsx";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
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

  // FIXME fix height of representation view

  return (
    <div className={classes.mainView}>
      <div className={classes.dataView}>
        <CanvasView imageUrl={url} />
        <div className="representationSelector">
          <Tabs defaultValue="MultiBallPercept" className="tabs-container">
            <TabsList className="grid h-full grid-rows tabs-list">
              <TabsTrigger value="MultiBallPercept">MultiBallPercept</TabsTrigger>
              <TabsTrigger value="BallModel">BallModel</TabsTrigger>
              <TabsTrigger value="TeamState">TeamState</TabsTrigger>
              <TabsTrigger value="ScanLineEdgelPercept">ScanLineEdgelPercept</TabsTrigger>
              <TabsTrigger value="FSRData">FSRData</TabsTrigger>
              <TabsTrigger value="BallCandidatesTop">BallCandidatesTop</TabsTrigger>
              <TabsTrigger value="CameraMatrixTop">CameraMatrixTop</TabsTrigger>
              <TabsTrigger value="TeamMessageDecision">TeamMessageDecision</TabsTrigger>
              <TabsTrigger value="MotionStatus">MotionStatus</TabsTrigger>
              <TabsTrigger value="ShortLinePercept">ShortLinePercept</TabsTrigger>
              <TabsTrigger value="RansacLinePercept">RansacLinePercept</TabsTrigger>
              <TabsTrigger value="ScanLineEdgelPerceptTop">ScanLineEdgelPerceptTop</TabsTrigger>
              <TabsTrigger value="InertialSensorData">InertialSensorData</TabsTrigger>
              <TabsTrigger value="RobotInfo">RobotInfo</TabsTrigger>
              <TabsTrigger value="GoalPercept">GoalPercept</TabsTrigger>
              <TabsTrigger value="FieldPerceptTop">FieldPerceptTop</TabsTrigger>
              <TabsTrigger value="MotorJointData">MotorJointData</TabsTrigger>
              <TabsTrigger value="CameraMatrix">CameraMatrix</TabsTrigger>
              <TabsTrigger value="SensorJointData">SensorJointData</TabsTrigger>
              <TabsTrigger value="ButtonData">ButtonData</TabsTrigger>
              <TabsTrigger value="RansacCirclePercept2018">RansacCirclePercept2018</TabsTrigger>
              <TabsTrigger value="FieldPercept">FieldPercept</TabsTrigger>
              <TabsTrigger value="AudioData">AudioData</TabsTrigger>
              <TabsTrigger value="GoalPerceptTop">GoalPerceptTop</TabsTrigger>
              <TabsTrigger value="BallCandidates">BallCandidates</TabsTrigger>
              <TabsTrigger value="OdometryData">OdometryData</TabsTrigger>
              <TabsTrigger value="FrameInfo">FrameInfo</TabsTrigger>
              <TabsTrigger value="AccelerometerData">AccelerometerData</TabsTrigger>
              <TabsTrigger value="IMUData">IMUData</TabsTrigger>
              <TabsTrigger value="GyrometerData">GyrometerData</TabsTrigger>
            </TabsList>
            <TabsContent value="MultiBallPercept" className="tabs-content">
            MultiBallPercept Data
            </TabsContent>
            <TabsContent value="GyrometerData">
              Change your password here.
            </TabsContent>
          </Tabs>
        </div>
      </div>

      <div className="p-4">
        <button onClick={() => setCamera("TOP")}>TOP</button>
        <button onClick={() => setCamera("BOTTOM")}>BOTTOM</button>
        <MultiRowRangeSlider length={images.length} />
      </div>
    </div>
  );
};

export default AnnotationView;
