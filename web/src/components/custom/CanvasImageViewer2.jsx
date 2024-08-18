import React, { useState, useRef, useEffect } from "react";
import { Stage, Layer, Image, Rect, Transformer } from 'react-konva';
import useImage from 'use-image';
import uuid4 from "uuid4";

const Rectangle = ({ shapeProps, isSelected, onSelect, onChange }) => {
  const shapeRef = React.useRef();
  const trRef = React.useRef();

  React.useEffect(() => {
    if (isSelected) {
      // we need to attach transformer manually
      trRef.current.nodes([shapeRef.current]);
      trRef.current.getLayer().batchDraw();
    }
  }, [isSelected]);

  return (
    <React.Fragment>
      <Rect
        onClick={onSelect}
        onTap={onSelect}
        ref={shapeRef}
        {...shapeProps}
        draggable
        onDragEnd={(e) => {
          onChange({
            ...shapeProps,
            x: e.target.x(),
            y: e.target.y(),
          });
        }}
        onTransformEnd={(e) => {
          // transformer is changing scale of the node
          // and NOT its width or height
          // but in the store we have only width and height
          // to match the data better we will reset scale on transform end
          const node = shapeRef.current;
          const scaleX = node.scaleX();
          const scaleY = node.scaleY();

          // we will reset it back
          node.scaleX(1);
          node.scaleY(1);
          onChange({
            ...shapeProps,
            x: node.x(),
            y: node.y(),
            // set minimal value
            width: Math.max(5, node.width() * scaleX),
            height: Math.max(node.height() * scaleY),
          });
        }}
      />
      {isSelected && (
        <Transformer
          ref={trRef}
          flipEnabled={false}
          boundBoxFunc={(oldBox, newBox) => {
            // limit resize
            if (Math.abs(newBox.width) < 5 || Math.abs(newBox.height) < 5) {
              return oldBox;
            }
            return newBox;
          }}
        />
      )}
    </React.Fragment>
  );
};

const initialRectangles = [
  {
    x: 10,
    y: 10,
    width: 100,
    height: 100,
    fill: 'red',
    id: uuid4(),
  },
  {
    x: 150,
    y: 150,
    width: 100,
    height: 100,
    fill: 'green',
    id: uuid4(),
  },
];

const CanvasImageViewer2 = ({ imageUrl }) => {
  const [image] = useImage(imageUrl);
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const [lastMousePosition, setLastMousePosition] = useState(null);
  const [boundingBoxes, setBoundingBoxes] = useState(initialRectangles);
  const [isDrawing, setIsDrawing] = useState(false);
  const stageRef = useRef(null);

  const [selectedId, selectShape] = React.useState(null);

  const checkDeselect = (e) => {
    // deselect when clicked on empty area
    const clickedOnEmpty = e.target === e.target.getStage();
    if (clickedOnEmpty) {
      selectShape(null);
    }
  };

  const canvasWidth = 640;
  const canvasHeight = 480;

  useEffect(() => {
    if (image) {
      const aspectRatio = image.width / image.height;
      const initialScale = Math.min(canvasWidth / image.width, canvasHeight / image.height);
      setScale(initialScale);
    }
  }, [image]);

  const getBoundedPosition = (newX, newY, newScale) => {
    const stage = stageRef.current;
    const minX = Math.min(0, canvasWidth - image.width * newScale);
    const maxX = 0;
    const minY = Math.min(0, canvasHeight - image.height * newScale);
    const maxY = 0;
    
    const x = Math.max(minX, Math.min(newX, maxX));
    const y = Math.max(minY, Math.min(newY, maxY));
    return { x, y };
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
    const minScale = Math.min(canvasWidth / image.width, canvasHeight / image.height);
    const finalScale = Math.max(newScale, minScale);
    
    const newPos = {
      x: -(mousePointTo.x - stage.getPointerPosition().x / finalScale) * finalScale,
      y: -(mousePointTo.y - stage.getPointerPosition().y / finalScale) * finalScale,
    };
    
    const boundedPos = getBoundedPosition(newPos.x, newPos.y, finalScale);
    setScale(finalScale);
    setPosition(boundedPos);
  };

  const handleMouseDown = (e) => {
    const stage = e.target.getStage();
    if (e.evt.button === 1) { // Middle mouse button
      e.evt.preventDefault(); // Prevent default middle-click behavior
      setIsPanning(true);
      setLastMousePosition(stage.getPointerPosition());
    } else if (e.evt.button === 0) { // Left mouse button
      const pos = stage.getRelativePointerPosition();
      setIsDrawing(true);
      const newBox = {
        x: pos.x,
        y: pos.y,
        width: 0,
        height: 0,
      };
      setBoundingBoxes([...boundingBoxes, newBox]);
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
    if (e.evt.button === 1) { // Middle mouse button
      setIsPanning(false);
      setLastMousePosition(null);
    } else if (e.evt.button === 0) { // Left mouse button
      setIsDrawing(false);
    }
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
      onMouseDown={checkDeselect}
      onTouchStart={checkDeselect}
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
                selectShape(box.id);
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
  );
};



export default CanvasImageViewer2;
