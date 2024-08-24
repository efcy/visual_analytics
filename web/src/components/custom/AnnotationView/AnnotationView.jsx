import { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import MultiRowRangeSlider from "../MultiRowRangeSlider/MultiRowRangeSlider";

import { useSelector } from "react-redux";
import DataView from "../DataView/DataView.jsx";
import CanvasView from "../CanvasView/CanvasView.jsx";
import classes from "./AnnotationView.module.css";

const AnnotationView = () => {
  const [imageList, setImageList] = useState([]);
  const [camera, setCamera] = useState("BOTTOM");
  const [url, setUrl] = useState("");
  const { id } = useParams();
  const store_idx = useSelector((state) => state.canvasReducer.index);

  useEffect(() => {
    get_image_data();
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
      })
      .catch((err) => alert(err));
  };

  useEffect(() => { 
    if (!imageList[store_idx]) {
      return;
    }
    const new_url =
      "https://logs.berlin-united.com/" + imageList[store_idx].image_url;
    setUrl(new_url);
  }, [store_idx, imageList]);

  return (
    <div className={classes.mainView}>
      <div className={classes.dataView}>
        <CanvasView imageUrl={url} setCamera={setCamera}/>
        <DataView />
      </div>

      <div className="p-4">
        <MultiRowRangeSlider length={imageList.length} />
      </div>
    </div>
  );
};

export default AnnotationView;
