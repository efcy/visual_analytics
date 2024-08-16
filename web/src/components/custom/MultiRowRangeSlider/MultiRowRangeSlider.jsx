import React, { useState, useRef, useEffect, useCallback } from "react";
import Draggable from "react-draggable";
import { useSelector, useDispatch } from "react-redux";
import { set } from "@/reducers/canvasSlice";
import classes from './MultiRowRangeSlider.module.css'


const MultiRowRangeSlider = ( {length} ) => {
  const [sliderValue, setSliderValue] = useState(0);
  const [stepSize, setStepSize] = useState(51);
  const [rows, setRows] = useState([
    { id: 1, type: "slider" },
    //{ id: 2, type: 'draggable', items: [{ id: 'item1', position: 0 }] },
    //{ id: 3, type: 'draggable', items: [{ id: 'item2', position: 0 }] },
  ]);
  const [containerWidth, setContainerWidth] = useState(0);
  const [gradientStyle, setGradientStyle] = useState({});
  const containerRef = useRef(null);

  const store_idx = useSelector((state) => state.canvasReducer.index);
  const dispatch = useDispatch();

  const maxValue = length;
  const totalBars = length;
  const minStepSize = 23; // Width of each bar including the indicator

  const updateGradientStyle = useCallback(() => {
    const newStyle = {
      backgroundImage: `repeating-linear-gradient(90deg, 
        var(--color-rose-bar) 0px ${stepSize - 1}px, 
        var(--color-rose-bar-indicator1) ${stepSize - 1}px ${stepSize}px)`,
      width: "100%",
      height: "100px",
    };
    setGradientStyle(newStyle);
  }, [stepSize]);

  useEffect(() => {
    const updateContainerWidth = () => {
      if (containerRef.current) {
        setContainerWidth(containerRef.current.offsetWidth);
      }
    };

    updateContainerWidth();
    window.addEventListener("resize", updateContainerWidth);
    return () => window.removeEventListener("resize", updateContainerWidth);
  }, []);

  useEffect(() => {
    updateGradientStyle();
  }, [stepSize, updateGradientStyle]);

  useEffect(() => {
    const handleScroll = (e) => {
      e.preventDefault();
      const delta_y = Math.sign(e.deltaY);
      const delta_x = Math.sign(e.deltaX);

      setStepSize((prevSize) => {
        const newSize = Math.max(minStepSize, Math.min(51, prevSize - delta_y));
        return newSize;
      });

      // handle horizontal scrolling in case you have a horizontal scrollwheel
      const currPos = container.scrollLeft;
      const scrollWidth = container.scrollWidth;
      const newPos = Math.max(0, Math.min(scrollWidth, currPos + delta_x * 18));
      container.scrollLeft = newPos;
    };

    const container = containerRef.current;
    if (container) {
      container.addEventListener("wheel", handleScroll, { passive: false });
    }

    return () => {
      if (container) {
        container.removeEventListener("wheel", handleScroll);
      }
    };
  }, [stepSize]);

  const handleSliderDrag = (e, data) => {
    const barIndex = Math.min(Math.floor(data.x / stepSize), totalBars - 1);
    const newValue = Math.round((barIndex / (totalBars - 1)) * maxValue);
    setSliderValue(newValue);

    // Scroll the container if the handle is near the edge
    if (containerRef.current) {
      const container = containerRef.current;
      const handleRight = data.x + stepSize;
      if (handleRight > container.scrollLeft + container.clientWidth) {
        container.scrollLeft = handleRight - container.clientWidth;
      } else if (data.x < container.scrollLeft) {
        container.scrollLeft = data.x;
      }
    }
  };

  const getHandlePosition = () => {
    const barIndex = Math.round((sliderValue / maxValue) * (totalBars - 1));
    dispatch(set(barIndex));
    console.log("position:", barIndex * stepSize + stepSize / 2, barIndex);
    return barIndex * stepSize + stepSize / 2;
  };

  const handleSliderClick = (e) => {
    if (containerRef.current) {
      const rect = containerRef.current.getBoundingClientRect();
      const clickX = e.clientX - rect.left + containerRef.current.scrollLeft;

      const barIndex = Math.min(Math.floor(clickX / stepSize), totalBars - 1);
      const newValue = Math.round((barIndex / (totalBars - 1)) * maxValue);
      setSliderValue(newValue);

      // Scroll to the clicked position if it's out of view
      const clickPosition = barIndex * stepSize;
      if (
        clickPosition < containerRef.current.scrollLeft ||
        clickPosition >
          containerRef.current.scrollLeft + containerRef.current.clientWidth
      ) {
        containerRef.current.scrollLeft =
          clickPosition - containerRef.current.clientWidth / 2;
      }
    }
  };

  const handleItemDrag = (rowId, itemId, e, data) => {
    const newPosition = Math.max(
      0,
      Math.min(data.x, containerWidth - stepSize)
    );

    setRows((prevRows) =>
      prevRows.map((row) =>
        row.id === rowId
          ? {
              ...row,
              items: row.items.map((item) =>
                item.id === itemId ? { ...item, position: newPosition } : item
              ),
            }
          : row
      )
    );
  };
  //FIXME make buttons work for previous and next, also make keyboard shortcuts work

  return (
    <>
      <button disabled={store_idx === 0}>Previous</button>
      <button>Next</button>
      <p>{store_idx}</p>

      <div className={classes.multi_row_range_slider} ref={containerRef}>
        {rows.map((row) => (
          <div
            key={row.id}
            className={classes.range_slider_container}
            style={{ width: `${stepSize * totalBars}px` }}
          >
            {row.type === "slider" ? (
              <div
                className={classes.customRange}
                style={gradientStyle}
                onClick={handleSliderClick}
              >
                <Draggable
                  axis="x"
                  bounds="parent"
                  grid={[stepSize, 0]}
                  onDrag={handleSliderDrag}
                  position={{ x: getHandlePosition(), y: 0 }}
                >
                  <div className={classes.rangeHandle}>
                    <span className={classes.rsValue}>{sliderValue}</span>
                  </div>
                </Draggable>
              </div>
            ) : (
              <div className={classes.draggableContainer}>
                {row.items.map((item) => (
                  <Draggable
                    key={item.id}
                    axis="x"
                    bounds="parent"
                    grid={[stepSize, 0]}
                    position={{ x: item.position, y: 0 }}
                    onDrag={(e, data) =>
                      handleItemDrag(row.id, item.id, e, data)
                    }
                  >
                    <div className={classes.dummy_video_track}>
                      Draggable Item {item.id}
                    </div>
                  </Draggable>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </>
  );
};

export default MultiRowRangeSlider;
