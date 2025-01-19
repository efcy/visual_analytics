let isDrawing = false;
let rect = null


function setUpCanvas(is_top, annotation_list, container_id){
    
    if(is_top){
        image_url = state.top_image.url
    }else{
        image_url = state.bottom_image.url
    }
    
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
        //console.log("konvaImage", konvaImage)
        layer.draw();
        draw_annotation(stage, is_top)
    };
}

function draw_annotation(stage, is_top){
    console.log("drawing on top image: ", is_top)
    if(is_top){
        image_id = state.top_image.id
        annotation_list = state.top_image.annotation
    }else{
        image_id = state.bottom_image.id
        annotation_list = state.bottom_image.annotation
    }
    const drawingLayer = new Konva.Layer();
    stage.add(drawingLayer);

    // load annotations if they exist
    console.log("annotation_list", annotation_list)
    console.log("image_id", image_id)
    if(!isObjectEmpty(annotation_list)){
        annotation_list.bbox.map((db_box, i) => {
            //console.log(db_box)
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
        //TODO somehow check if you click on a rectangle and have this selected to be able to refer to that
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
        bbox = {
            height: rect.height(),
            width: rect.width(),
            id: crypto.randomUUID(),
            x: rect.x(),
            y: rect.y(),
            label: "ball",
        }
        //TODO add bounding box to annotation list
        console.log("annotation_list: ", annotation_list)
        annotation_list.bbox.push(bbox)
        console.log("after:", annotation_list)
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        

        ///*
        fetch(state.api_url, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ 
                image: image_id,
                annotations: annotation_list 
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log("Success:", data);
        })
        .catch(error => {
            console.error("Error:", error);
        });
        //*/
    }

    stage.on("mousedown", mousedownhandler);
    stage.on("mousemove", mousemovehandler)
    stage.on("mouseup", mouseuphandler)
}
