import { useState, useEffect } from 'react';

const useImageLoader = (id, frameNumber, api) => {
  const [state, setState] = useState({
    topImage: null,
    bottomImage: null,
    isLoading: false,
    error: null
  });

  const loadFallbackImage = async () => {
    const fallbackImg = new Image();
    return new Promise((resolve) => {
      fallbackImg.onload = () => resolve(fallbackImg);
      fallbackImg.onerror = () => resolve(null); // In case even fallback fails
      fallbackImg.src = "https://www.dummyimage.co.uk/640x480/cbcbcb/959595/No%20Image%20available/40";
    });
  };

  const loadImageFromUrl = async (imageData, camera) => {
    if (!imageData || !imageData.length) {
      return loadFallbackImage();
    }

    const imageUrl = "https://logs.berlin-united.com/" + imageData[0].image_url;
    
    try {
      const img = new Image();
      
      const imageLoadPromise = new Promise((resolve) => {
        img.onload = () => resolve(img);
        img.onerror = () => resolve(loadFallbackImage());
        img.src = imageUrl;
      });

      return imageLoadPromise;
    } catch {
      return loadFallbackImage();
    }
  };

  const fetchImageData = async (camera) => {
    try {
      const response = await api.get(
        `${import.meta.env.VITE_API_URL}/api/image/?log=${id}&camera=${camera}&frame_number=${frameNumber}`
      );
      return response.data;
    } catch {
      // Return null to indicate API failure
      return null;
    }
  };

  const loadImages = async () => {
    setState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      // Fetch both image metadata in parallel
      const [topData, bottomData] = await Promise.all([
        fetchImageData('TOP'),
        fetchImageData('BOTTOM')
      ]);

      // Load both images in parallel
      const [topImage, bottomImage] = await Promise.all([
        loadImageFromUrl(topData, 'TOP'),
        loadImageFromUrl(bottomData, 'BOTTOM')
      ]);

      setState({
        topImage,
        bottomImage,
        isLoading: false,
        error: null
      });
    } catch (error) {
      console.log("failed to load images", error.message  )
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error.message || 'Failed to load images'
      }));
    }
  };

  // Load images when frameNumber changes
  useEffect(() => {
    loadImages();
  }, [frameNumber, id]);

  return {
    topImage: state.topImage,
    bottomImage: state.bottomImage,
    isLoading: state.isLoading,
    error: state.error,
    reloadImages: loadImages
  };
};

export default useImageLoader;