import React from "react";
import { Stage, Layer, Rect, Transformer } from "react-konva";

const initialRectangles = [
  {
    x: 10,
    y: 10,
    width: 100,
    height: 100,
    fill: "red",
    id: "rect1",
  },
  {
    x: 150,
    y: 150,
    width: 100,
    height: 100,
    fill: "green",
    id: "rect2",
  },
];

const KonvaViewer = () => {
  const [rectangles, setRectangles] = React.useState(initialRectangles);
  const [selectedId, selectShape] = React.useState(null);

  const checkDeselect = (e) => {
    // deselect when clicked on empty area
    const clickedOnEmpty = e.target === e.target.getStage();
    if (clickedOnEmpty) {
      selectShape(null);
    }
  };

  <Stage
    width={500}
    height={500}
    onMouseDown={checkDeselect}
    onTouchStart={checkDeselect}
  >
    <Layer>
      {rectangles.map((rect, i) => {
        return (
          <Rectangle
            key={i}
            shapeProps={rect}
            isSelected={rect.id === selectedId}
            onSelect={() => {
              selectShape(rect.id);
            }}
            onChange={(newAttrs) => {
              const rects = rectangles.slice();
              rects[i] = newAttrs;
              setRectangles(rects);
            }}
          />
        );
      })}
    </Layer>
  </Stage>;
};

export default KonvaViewer;
