// taken from https://www.youtube.com/watch?v=i1PN_c5DmaI
import { useState, useEffect } from "react";

const useDebounce = (val, delay) => {
  const [debounceVal, setDebounceVal] = useState(val);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebounceVal(val);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [val]);

  return debounceVal;
};

export default useDebounce;
