import Konva from "konva";
import { useState, useRef, useEffect } from "react";
import { Stage, Layer, Image } from "react-konva";
import uuid4 from "uuid4";
import Rectangle from "../Rectangle/Rectangle";
import classes from "./CanvasView.module.css";
import { ToggleGroup, ToggleGroupItem } from "@/components/ui/toggle-group";
import { Button } from "@/components/ui/button";

const CanvasView = ({
  image,
  currentCamera,
  setCamera,
  setFrameFilter,
  annotations,
}) => {
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const [lastMousePosition, setLastMousePosition] = useState(null);
  const [boundingBoxes, setBoundingBoxes] = useState([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const [selectedId, setSelectedId] = useState(null);
  const [selectedCamera, setSelectedCamera] = useState(currentCamera);
  const stageRef = useRef(null);
  const cameraList = ["TOP", "BOTTOM"];
  const canvasWidth = 640;
  const canvasHeight = 480;

  const click = (value) => {
    setSelectedCamera(value);
    setCamera(value);
  };

  useEffect(() => {
    //TODO eventually load the existing annotations here

    if (annotations) {
      console.log(annotations);
      console.log(annotations.annotation.bbox);

      console.log("load bounding boxes from annotations from db");
      const db_boxes = [];
      annotations.annotation.bbox.map((db_box, i) => {
        console.log(i, db_box);
        const newBox = {
          x: db_box.x,
          y: db_box.y,
          width: db_box.width,
          height: db_box.height,
          fill: "rgba(0, 255, 0, 0.5)",
          stroke: "rgba(0, 255, 0, 1)",
          strokeWidth: 2,
          opacity: 0.5,
          id: uuid4(),
        };
        db_boxes.push(newBox);
      });
      //setBoundingBoxes([...boundingBoxes, ...db_boxes]);
    } else {
      setBoundingBoxes([]);
    }
  }, [image, annotations]); // this list is called dependency array

  const checkDeselect = (e) => {
    // deselect when clicked on empty area
    const clickedOnEmpty =
      e.target === e.target.getStage() || e.target.attrs.name === undefined;
    if (clickedOnEmpty) {
      setSelectedId(null);
    }
  };

  const getBoundedPosition = (newX, newY, newScale) => {
    const minX = Math.min(0, canvasWidth - image.width * newScale);
    const maxX = 0;
    const minY = Math.min(0, canvasHeight - image.height * newScale);
    const maxY = 0;

    const x = Math.max(minX, Math.min(newX, maxX));
    const y = Math.max(minY, Math.min(newY, maxY));
    return { x, y };
  };

  const updateBoundingBoxes = () => {
    try {
      console.log("updateBoundingBoxes");
      //const res = api.post("/api/annotations/", { a: "asd" });
    } catch (error) {
      alert(error);
    }
  };

  const handleWheel = (e) => {
    e.evt.preventDefault();
    const scaleBy = 1.1;
    const stage = stageRef.current;
    const oldScale = stage.scaleX();
    const mousePointTo = {
      x: stage.getPointerPosition().x / oldScale - stage.x() / oldScale,
      y: stage.getPointerPosition().y / oldScale - stage.y() / oldScale,
    };
    const newScale = e.evt.deltaY < 0 ? oldScale * scaleBy : oldScale / scaleBy;
    const minScale = Math.min(
      canvasWidth / image.width,
      canvasHeight / image.height,
    );
    const finalScale = Math.max(newScale, minScale);

    const newPos = {
      x:
        -(mousePointTo.x - stage.getPointerPosition().x / finalScale) *
        finalScale,
      y:
        -(mousePointTo.y - stage.getPointerPosition().y / finalScale) *
        finalScale,
    };

    const boundedPos = getBoundedPosition(newPos.x, newPos.y, finalScale);
    setScale(finalScale);
    setPosition(boundedPos);
  };

  const handleMouseDown = (e) => {
    checkDeselect(e);
    const stage = e.target.getStage();
    if (e.evt.button === 1) {
      // Middle mouse button
      e.evt.preventDefault(); // Prevent default middle-click behavior
      setIsPanning(true);
      setLastMousePosition(stage.getPointerPosition());
    } else if (e.evt.button === 0) {
      // Left mouse button
      const pos = stage.getRelativePointerPosition();
      // check if we actually click on the image
      const shape = stage.getIntersection(pos);
      if (shape instanceof Konva.Image) {
        setIsDrawing(true);
        const newBox = {
          x: pos.x,
          y: pos.y,
          width: 0,
          height: 0,
          fill: "rgba(0, 255, 0, 0.5)",
          stroke: "rgba(0, 255, 0, 1)",
          strokeWidth: 2,
          opacity: 0.5,
          id: uuid4(),
        };
        console.log("handleMouseDown");
        setBoundingBoxes([...boundingBoxes, newBox]);
      }
    }
  };

  const handleMouseMove = (e) => {
    const stage = e.target.getStage();
    if (isPanning && lastMousePosition) {
      const newMousePosition = stage.getPointerPosition();
      const deltaX = newMousePosition.x - lastMousePosition.x;
      const deltaY = newMousePosition.y - lastMousePosition.y;
      const newPos = {
        x: position.x + deltaX,
        y: position.y + deltaY,
      };
      const boundedPos = getBoundedPosition(newPos.x, newPos.y, scale);
      setPosition(boundedPos);
      setLastMousePosition(newMousePosition);
    } else if (isDrawing) {
      const pos = stage.getRelativePointerPosition();
      const lastBox = boundingBoxes[boundingBoxes.length - 1];
      const newBox = {
        ...lastBox,
        width: pos.x - lastBox.x,
        height: pos.y - lastBox.y,
      };
      const updatedBoxes = [...boundingBoxes];
      updatedBoxes[boundingBoxes.length - 1] = newBox;
      setBoundingBoxes(updatedBoxes);
    }
  };

  const handleMouseUp = (e) => {
    if (e.evt.button === 1) {
      // Middle mouse button
      setIsPanning(false);
      setLastMousePosition(null);
    } else if (e.evt.button === 0) {
      // Left mouse button
      setIsDrawing(false);
      console.log("boundingBoxes: ", boundingBoxes);
      //TODO add post request here for annotation
      updateBoundingBoxes();
    }
  };

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Delete" && selectedId) {
        deleteSelectedRect();
      }
    };

    window.addEventListener("keydown", handleKeyDown);

    // Cleanup
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
    };
  }, [selectedId]); // Re-run effect if selectedId changes

  const deleteSelectedRect = () => {
    setBoundingBoxes((prevBoxes) =>
      prevBoxes.filter((box) => box.id !== selectedId),
    );
    setSelectedId(null);
  };

  const toggle_frame_filter = () => {
    setFrameFilter((prevValue) => (prevValue === 0 ? 1 : 0));
  };

  return (
    <div className={classes.canvasView}>
      <Stage
        width={canvasWidth}
        height={canvasHeight}
        onWheel={handleWheel}
        scaleX={scale}
        scaleY={scale}
        x={position.x}
        y={position.y}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        ref={stageRef}
      >
        <Layer>
          <Image image={image} />
        </Layer>
        <Layer>
          {boundingBoxes.map((box, i) => (
            <Rectangle
              key={i}
              shapeProps={box}
              isSelected={box.id === selectedId}
              onSelect={() => {
                setIsDrawing(false);
                setSelectedId(box.id);
              }}
              onChange={(newAttrs) => {
                const rects = boundingBoxes.slice();
                rects[i] = newAttrs;
                setBoundingBoxes(rects);
              }}
              strokeWidth={2 / scale}
            />
          ))}
        </Layer>
      </Stage>
      <div className={classes.controls}>
        <ToggleGroup
          type="single"
          defaultValue={selectedCamera.toString()}
          value={selectedCamera.toString()}
          className=""
          onValueChange={(value) => {
            if (value) {
              click(value);
            }
          }}
        >
          {cameraList.map((value) => {
            return (
              <ToggleGroupItem
                variant="outline"
                key={value}
                value={value.toString()}
                aria-label={`Toggle ${value}`}
                className="data-[state=on]:bg-red-200"
              >
                {value}
              </ToggleGroupItem>
            );
          })}
        </ToggleGroup>
        <Button onClick={() => toggle_frame_filter(1)}>FrameFilter</Button>
      </div>
    </div>
  );
};

export default CanvasView;
