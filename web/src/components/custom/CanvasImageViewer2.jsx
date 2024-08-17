import React, { useState, useRef, useEffect } from "react";
import { Stage, Layer, Image, Rect } from 'react-konva';
import useImage from 'use-image';

const CanvasImageViewer2 = ({ imageUrl }) => {
  const [image] = useImage(imageUrl);
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [boundingBoxes, setBoundingBoxes] = useState([]);
  const [isDrawing, setIsDrawing] = useState(false);
  const stageRef = useRef(null);

  const canvasWidth = 640;
  const canvasHeight = 480;

  useEffect(() => {
    if (image) {
      const aspectRatio = image.width / image.height;
      const initialScale = Math.min(canvasWidth / image.width, canvasHeight / image.height);
      setScale(initialScale);
    }
  }, [image]);

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
    const minScale = Math.min(canvasWidth / image.width, canvasHeight / image.height);
    const finalScale = Math.max(newScale, minScale);
    setScale(finalScale);
    setPosition({
      x: -(mousePointTo.x - stage.getPointerPosition().x / finalScale) * finalScale,
      y: -(mousePointTo.y - stage.getPointerPosition().y / finalScale) * finalScale,
    });
  };

  const handleMouseDown = (e) => {
    //const { x, y } = e.target.getStage().getPointerPosition();
    setIsDrawing(true);
    console.log("setIsDrawing")
    const pos = stageRef.current.getPointerPosition();
    const newBox = {
      x: (pos.x - position.x) / scale,
      y: (pos.y - position.y) / scale,
      width: 0,
      height: 0,
    }
      setBoundingBoxes([...boundingBoxes, newBox]);
  };

  const handleMouseMove = (e) => {
    
    if (!isDrawing) return;
    console.log("mouse move")
    const pos = stageRef.current.getPointerPosition();
    const lastBox = boundingBoxes[boundingBoxes.length - 1];
    const newBox = {
      ...lastBox,
      width: (pos.x - position.x) / scale - lastBox.x,
      height: (pos.y - position.y) / scale - lastBox.y,
    };
    const updatedBoxes = [...boundingBoxes];
    console.log(newBox)
    updatedBoxes[boundingBoxes.length - 1] = newBox;
    setBoundingBoxes(updatedBoxes);
  };

  const handleMouseUp = () => {
    setIsDrawing(false);
  };

  return (
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
          <Rect
            key={i}
            x={box.x}
            y={box.y}
            width={box.width}
            height={box.height}
            stroke="red"
            strokeWidth={2 / scale}
          />
        ))}
      </Layer>
    </Stage>
  );
};



export default CanvasImageViewer2;
