import React from "react";
import { Stage, Layer, Rect, Transformer, Circle } from 'react-konva';


const CanvasImageViewer = () => {

  console.log(window.innerWidth)
  return (
    <Stage
      width={window.innerWidth}
      height={window.innerHeight}
    
      className="stage"
    >
      <Layer>
      <Circle x={200} y={100} radius={50} fill="green" draggable />
      </Layer>
    </Stage>
  );
};



export default CanvasImageViewer;
