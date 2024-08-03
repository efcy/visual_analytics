import React, { useState, useEffect } from 'react';

const FrameTimeline = ({ frames, width = 500 }) => {
  const [sliderValue, setSliderValue] = useState(0);

  const formatTime = (milliseconds) => {
    const seconds = milliseconds / 1000;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toFixed(0).padStart(2, '0')}`;
  };

  const totalDuration = frames[frames.length - 1].time;

  const generateMinuteTicks = () => {
    const ticks = [];
    for (let time = 0; time <= totalDuration; time += 60000) {
      const position = (time / totalDuration) * 100;
      ticks.push({ time, position });
    }
    return ticks;
  };

  const minuteTicks = generateMinuteTicks();

  const handleSliderChange = (e) => {
    const newValue = parseFloat(e.target.value);
    setSliderValue(newValue);
    const selectedFrame = frames[Math.round(newValue)];
    console.log(`Selected frame: ${selectedFrame.framenumber}, Time: ${formatTime(selectedFrame.time)}, Data: ${selectedFrame.data}`);
  };

  const getCurrentFrameInfo = () => {
    const selectedFrame = frames[Math.round(sliderValue)];
    return `Frame: ${selectedFrame.framenumber}, Time: ${formatTime(selectedFrame.time)}, Data: ${selectedFrame.data}`;
  };

  useEffect(() => {
    console.log(`Initial frame: ${frames[0].framenumber}, Time: ${formatTime(frames[0].time)}, Data: ${frames[0].data}`);
  }, [frames]);

  return (
    <div className="relative" style={{ width: `${width}px`, height: '100px' }}>
      <div className="absolute w-full h-1 bg-gray-300 top-8"></div>
      {minuteTicks.map(({ time, position }, index) => (
        <div
          key={index}
          className="absolute transform"
          style={{ left: `${position}%`, top: '28px' }}
        >
          <div className="w-0.5 h-4 bg-gray-500"></div>
          <div className="mt-1 text-xs text-center whitespace-nowrap">
            {formatTime(time)}
          </div>
        </div>
      ))}
      <input
        type="range"
        min="0"
        max={frames.length - 1}
        step="1"
        value={sliderValue}
        onChange={handleSliderChange}
        className="absolute w-full top-7 appearance-none bg-transparent 
          [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-1 [&::-webkit-slider-thumb]:h-6 [&::-webkit-slider-thumb]:bg-blue-500 [&::-webkit-slider-thumb]:cursor-pointer
          [&::-moz-range-thumb]:appearance-none [&::-moz-range-thumb]:w-1 [&::-moz-range-thumb]:h-6 [&::-moz-range-thumb]:bg-blue-500 [&::-moz-range-thumb]:cursor-pointer
          [&::-ms-thumb]:appearance-none [&::-ms-thumb]:w-1 [&::-ms-thumb]:h-6 [&::-ms-thumb]:bg-blue-500 [&::-ms-thumb]:cursor-pointer"
        style={{
          left: '0',
          right: '0',
          margin: '0 auto',
          width: '100%',
        }}
      />
      <div className="absolute top-16 left-0 right-0 text-center text-sm font-semibold">
        {getCurrentFrameInfo()}
      </div>
    </div>
  );
};

export default FrameTimeline;