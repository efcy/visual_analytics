let isDrawing = false;
let rect = null

const isObjectEmpty = (objectName) => {
    // generic function for checking if an javascript object is empty
    // we use it for checking for an empty annotation json
    return (
      objectName &&
      Object.keys(objectName).length === 0 &&
      objectName.constructor === Object
    );
  };

function setUpCanvas(image_url, annotation_list, container_id){
    console.log(image_url, container_id)
    
    const stage = new Konva.Stage({
        container: container_id,
        width: 640,
        height: 480,
    });
    const layer = new Konva.Layer();
    stage.add(layer);
    
    const imageObj = new Image();
    imageObj.src = image_url;

    imageObj.onload = function() {        
        // Create Konva image
        const konvaImage = new Konva.Image({
            image: imageObj,
            width: 640,
            height: 480,
        });
        
        layer.add(konvaImage);
        console.log("konvaImage", konvaImage)
        layer.draw();
        draw_annotation(stage, annotation_list)
    };
}

function draw_annotation(stage, annotation_list){
    const drawingLayer = new Konva.Layer();
    stage.add(drawingLayer);

    // load annotations if they exist
    if(!isObjectEmpty(annotation_list)){
        annotation_list.bbox.map((db_box, i) => {
            console.log(db_box)
            var rect = new Konva.Rect({
                x: db_box.x,
                y: db_box.y,
                width: db_box.width,
                height: db_box.height,
                fill: "rgba(0, 255, 0, 0.5)",
                stroke: "rgba(0, 255, 0, 1)",
                strokeWidth: 2,
                name: 'rect',
                strokeScaleEnabled: false,
                opacity: 0.5,
                draggable: true,
            });
            drawingLayer.add(rect);
        });
    }

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
    drawingLayer.add(tr);
    //tr.nodes([rect]);

    stage.on("click tap", (e) => {
    // If we click on nothing clear the transformer and update the layer
    if (e.target === stage) {
        tr.nodes([]);
        layer.batchDraw();
        return;
    }
    
    // Add the selected element to the transformer and update the layer
    tr.nodes([e.target]);
    drawingLayer.batchDraw();
    });

    function mousedownhandler(){
        const pos = stage.getRelativePointerPosition();
        const shape = stage.getIntersection(pos);
        if (shape instanceof Konva.Image) {
            isDrawing = true;
            rect = new Konva.Rect({
                x: stage.getPointerPosition().x,
                y: stage.getPointerPosition().y,
                width: 0,
                height: 0,
                fill: "rgba(0, 255, 0, 0.5)",
                stroke: "rgba(0, 255, 0, 1)",
                strokeWidth: 2,
                strokeScaleEnabled: false,
                opacity: 0.5,
                draggable: true,
            });
            drawingLayer.add(rect).batchDraw();
        }
    }
    function mousemovehandler(){
        if(!isDrawing){
            return false;
        }
        const newWidth = stage.getPointerPosition().x - rect.x();
        const newHeight = stage.getPointerPosition().y - rect.y();
        rect.width(newWidth).height(newHeight);
    }
    
    function mouseuphandler(){
        isDrawing = false;
    }

    stage.on("mousedown", mousedownhandler);
    stage.on("mousemove", mousemovehandler)
    stage.on("mouseup", mouseuphandler)
}
