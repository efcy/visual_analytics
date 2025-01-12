const stages = new Map();

function test(){
    elem = document.getElementById("konva-container1")
    console.log(elem.offsetWidth)
}

function setUpCanvas(image_url, container_id){
    console.log(image_url, container_id)
    
    const stage = new Konva.Stage({
        container: container_id,
        width: 640,
        height: 480,
    });
    const layer = new Konva.Layer();
    stage.add(layer);

    // Update stage size to match container
    const container = stage.container();

    // Store stage reference
    stages.set(container_id, { stage, layer });
    
    const imageObj = new Image();
    imageObj.src = image_url;

    imageObj.onload = function() {
        
        const imageAspectRatio = imageObj.width / imageObj.height;
        console.log(imageAspectRatio)
        const targetAspectRatio = 4/3;

        // Get container dimensions
        const container = stage.container();
        const containerWidth = container.offsetWidth;
        const containerHeight = container.offsetHeight;

        // Update stage size to match container
        //stage.width(containerWidth);
        //stage.height(containerHeight);

        // Calculate dimensions to maintain aspect ratio
        let imageWidth, imageHeight;
        if (imageAspectRatio > targetAspectRatio) {
            // Image is wider than target ratio
            imageWidth = containerWidth;
            imageHeight = containerWidth / imageAspectRatio;
        } else {
            // Image is taller than target ratio
            imageHeight = containerHeight;
            imageWidth = containerHeight * imageAspectRatio;
        }

        // Create Konva image
        const konvaImage = new Konva.Image({
            image: imageObj,
            width: 640,
            height: 480,
        });
        
        layer.add(konvaImage);
        console.log("konvaImage", konvaImage)
        layer.draw();
        draw_annotation(stage)
    };
}

function draw_annotation(stage){
    const drawingLayer = new Konva.Layer();
    stage.add(drawingLayer);
    var rect = new Konva.Rect({
        x: 160,
        y: 60,
        width: 100,
        height: 90,
        fill: "rgba(0, 255, 0, 0.5)",
        stroke: "rgba(0, 255, 0, 1)",
        strokeWidth: 2,
        name: 'rect',
        strokeScaleEnabled: false,
        opacity: 0.5,
        draggable: true,
      });
      drawingLayer.add(rect);

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

      rect.on('transformstart', function () {
        console.log('transform start');
      });

      rect.on('dragmove', function () {

      });
      rect.on('transform', function () {

        console.log('transform');
      });

      rect.on('transformend', function () {
        console.log('transform end');
      });

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
}