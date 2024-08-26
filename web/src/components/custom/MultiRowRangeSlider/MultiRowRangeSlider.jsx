import React, { useState, useRef, useEffect, useCallback } from "react";
import Draggable from "react-draggable";
import { useSelector, useDispatch } from "react-redux";
import { set } from "@/reducers/canvasSlice";
import classes from './MultiRowRangeSlider.module.css'
import { Button } from "@/components/ui/button"

const MultiRowRangeSlider = ( {length} ) => {
  console.log("MultiRowRangeSlider called", length)
  const [sliderValue, setSliderValue] = useState(0);
  const [stepSize, setStepSize] = useState(51);
  const [gradientStyle, setGradientStyle] = useState({});
  const containerRef = useRef(null);
  const draggableRef = React.useRef(null);

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
    updateGradientStyle();
  }, [stepSize, updateGradientStyle]);

  const previous_frame = ( step = 1 ) => {
    const stepValue = step === undefined ? 1 : Number(step);
    setSliderValue(prevValue => prevValue - stepValue);
  }
  const next_frame = ( step = 1 ) => {
    
    const stepValue = step === undefined ? 1 : Number(step);
    setSliderValue(prevValue => prevValue + stepValue);
  }

  const handleKeyPress = useCallback((event) => {
    switch(event.key) {
      // FIXME make step configurable
      case 'ArrowRight':
        if (store_idx < length - 1) {
          next_frame(1);
        }
        break;
      case 'ArrowLeft':
        if (store_idx > 0) {
          previous_frame(1);
        }
        break;
      default:
        console.log(`Key pressed: ${event.key}`);
    }
  }, [store_idx, length, next_frame, previous_frame]);

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

  useEffect(() => {
    // attach the event listener
    document.addEventListener('keydown', handleKeyPress);
    // remove the event listener
    return () => {
      document.removeEventListener('keydown', handleKeyPress);
    };
  }, [handleKeyPress]);

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


  return (
    <>
      <Button disabled={store_idx === 0} onClick={() => previous_frame(1)}>Previous</Button>
      <Button disabled={store_idx === length -1} onClick={() => next_frame(1)}>Next</Button>
      <p>{store_idx}</p>

      <div className={classes.multi_row_range_slider} ref={containerRef}>
          <div
            className={classes.range_slider_container}
            style={{ width: `${stepSize * totalBars}px` }}
          >
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
                  nodeRef={draggableRef}
                >
                  <div className={classes.rangeHandle} ref={draggableRef}>
                    <span className={classes.rsValue}>{sliderValue}</span>
                  </div>
                </Draggable>
              </div>
          </div>
      </div>
    </>
  );
};

export default MultiRowRangeSlider;
