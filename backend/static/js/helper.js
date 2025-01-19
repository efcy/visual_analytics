const isObjectEmpty = (objectName) => {
  // generic function for checking if an javascript object is empty
  // we use it for checking for an empty annotation json
  return (
    objectName &&
    Object.keys(objectName).length === 0 &&
    objectName.constructor === Object
  );
};

const generateUUID4 = () =>{
  // similar to what python would return
  return crypto.randomUUID().replace(/-/g,"").slice(0,9).toUpperCase();
}

const getBoundingBoxTransformer = () => {
  // create new transformer
  var tr = new Konva.Transformer();
  tr.rotateEnabled(false);
  tr.flipEnabled(false);
  tr.anchorStroke("green");
  tr.anchorFill('white');
  tr.keepRatio(false);
  tr.ignoreStroke(true);
  tr.borderStrokeWidth(0);
  tr.enabledAnchors([
      "top-left",
      "top-right",
      "bottom-left",
      "bottom-right",
  ]);
  tr.anchorCornerRadius(10);

  return tr;
}