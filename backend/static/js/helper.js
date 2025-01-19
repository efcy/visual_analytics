const isObjectEmpty = (objectName) => {
    // generic function for checking if an javascript object is empty
    // we use it for checking for an empty annotation json
    return (
      objectName &&
      Object.keys(objectName).length === 0 &&
      objectName.constructor === Object
    );
  };