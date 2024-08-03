import React, { useState, useEffect } from 'react';

const Timeline = ({ endTimeInSeconds, width = 500}) => {
  const [sliderValue, setSliderValue] = useState(0);

  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toFixed(0).padStart(2, '0')}`;
  };
  
  const generateTicks = () => {
    const ticks = [];
    for (let time = 0; time <= endTimeInSeconds; time += 60) {
      const position = (time / endTimeInSeconds) * 100;
      ticks.push({ time, position });
    }
    // Ensure the last tick is at the end time if it's not exactly on a minute mark
    if (endTimeInSeconds % 60 !== 0) {
      ticks.push({ time: endTimeInSeconds, position: 100 });
    }
    return ticks;
  };
  const ticks = generateTicks();

  const handleSliderChange = (e) => {
    const newValue = parseFloat(e.target.value);
    setSliderValue(newValue);
    const currentSeconds = (newValue / 100) * endTimeInSeconds;
    console.log(`Slider value: ${newValue}, Current seconds: ${currentSeconds.toFixed(2)}`);
  };

  useEffect(() => {
    console.log(`Initial time: ${formatTime(0)} (0 seconds)`);
  }, []);

  return (
    <div className="relative" style={{ width: `${width}px`, height: '100px' }}>
      <div className="absolute w-full h-1 bg-gray-300 top-8"></div>
      {ticks.map(({ time, position }, index) => (
        <div
          key={index}
          className="absolute transform "
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
        max="100"
        step="0.01"
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
        Current: {formatTime((sliderValue / 100) * endTimeInSeconds)}
      </div>
    </div>
  );
};

export default Timeline;