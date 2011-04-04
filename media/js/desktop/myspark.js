var initSpark = function (level) {
    var canvas = document.getElementById('spark'),
        ctx = canvas.getContext("2d"),
        h = $('#spark-graphic').height(),
    	w = $('#spark-graphic').width(),
    	shapes = [];

    canvas.height = h;
    canvas.width = w;

    var deg2rad = function(degrees) {
    	return degrees * Math.PI/180;
    };

    var rand = function(min, max) {
        return min + Math.floor(Math.random() * (max - min));
    };

    var drawShapes = function(shapes, level) {

        for(i = 0, nb = shapes[level - 1].length; i < nb; i += 1) {
            var shape = shapes[level - 1][i];
            
         	ctx.save();
                ctx.shadowBlur = 30;
                ctx.shadowColor = "rgba(0,0,0,0.3)";
    	    	ctx.fillStyle = "rgba("+shape.rgb+", 0.6)";
    		    ctx.translate(w / 2, h);
    	        ctx.rotate(deg2rad(shape.angle));
    	        ctx.beginPath();
    	        ctx.moveTo(0, 0);
    	        ctx.arc(0, 0, 100 * shape.scale, 0, -deg2rad(shape.arcAngle), true);
    	        ctx.fill();
    	    ctx.restore();
        }
    };

    var update = function() {
        var dice;
        for(var i = 0, nb = shapes[level - 1].length; i < nb; i += 1) {
            var s = shapes[level - 1][i],
                dice = rand(1, 6);

            s.moveFactor = 1-(i/6);
            
            if(Math.abs(s.angle) > (s.maxAngle - s.arcAngle) || Math.abs(s.angle) < s.minAngle || dice === 6) {
                s.angleStep *= -1;
            } 
            s.angle += s.angleStep * rand(1, 2);

            if(s.scale > s.maxScale || s.scale < s.minScale || dice === 1) {
                s.scaleStep *= -1;
            }
            s.scale += s.scaleStep * rand(1, 2);
        }
    };

    var initShapes = function() {
        shapes = [ 
                    //level 1
                    [
                        { arcAngle: 80, angle: -20, angleStep: -0.2, minAngle: 20, maxAngle: 110, rgb: '255, 0, 60', scale: 0.75, scaleStep: 0.005, minScale: 0.7, maxScale: 0.8 },
                        { arcAngle: 80, angle: -40, angleStep: -0.3, minAngle: -15, maxAngle: -50, rgb: '255, 0, 60', scale: 0.65, scaleStep: 0.005, minScale: 0.6, maxScale: 0.7 },
                        { arcAngle: 80, angle: -65, angleStep: -0.2, minAngle: -40, maxAngle: -80, rgb: '255, 155, 0', scale: 0.55, scaleStep: 0.005, minScale: 0.5, maxScale: 0.6 },
                        { arcAngle: 95, angle: -2, angleStep: -0.2, minAngle: 0, maxAngle: -20, rgb: '255, 155, 0', scale: 0.45, scaleStep: 0.005, minScale: 0.4, maxScale: 0.5 },
                        { arcAngle: 105, angle: -55, angleStep: -0.25, minAngle: -50, maxAngle: -75, rgb: '255, 255, 0', scale: 0.35, scaleStep: 0.005, minScale: 0.3, maxScale: 0.4 },
                        { arcAngle: 105, angle: -75, angleStep: -0.005, minAngle: -60, maxAngle: -100, rgb: '255, 255, 0', scale: 0.25, scaleStep: 0.005, minScale: 0.2, maxScale: 0.3 }
                    ],
                    //level 2
                    [
                        { arcAngle: 85, angle: -60, angleStep: -0.2, minAngle: 45, maxAngle: 140, rgb: '255, 0, 60', scale: 0.95, scaleStep: 0.005, minScale: 0.9, maxScale: 1 },
                        { arcAngle: 85, angle: -15, angleStep: -0.2, minAngle: 15, maxAngle: 110, rgb: '255, 0, 60', scale: 0.85, scaleStep: 0.005, minScale: 0.8, maxScale: 0.9 },
                        { arcAngle: 80, angle: -50, angleStep: -0.2, minAngle: 35, maxAngle: 120, rgb: '255, 0, 60', scale: 0.75, scaleStep: 0.005, minScale: 0.7, maxScale: 0.8 },
                        { arcAngle: 80, angle: -80, angleStep: -0.2, minAngle: 60, maxAngle: 150, rgb: '255, 155, 0', scale: 0.65, scaleStep: 0.005, minScale: 0.6, maxScale: 0.7 },
                        { arcAngle: 105, angle: -35, angleStep: -0.25, minAngle: 25, maxAngle: 145, rgb: '255, 255, 0', scale: 0.45, scaleStep: 0.005, minScale: 0.4, maxScale: 0.5 },
                        { arcAngle: 95, angle: -2, angleStep: -0.2, minAngle: 0, maxAngle: -20, rgb: '255, 155, 0', scale: 0.55, scaleStep: 0.005, minScale: 0.5, maxScale: 0.6 },
                        { arcAngle: 105, angle: -75, angleStep: -0.005, minAngle: -60, maxAngle: -100, rgb: '255, 255, 0', scale: 0.35, scaleStep: 0.005, minScale: 0.3, maxScale: 0.4 }
                    ],
                    //level 3
                    [
                        { arcAngle: 88, angle: -55, angleStep: -0.2, minAngle: 30, maxAngle: 160, rgb: '255, 0, 60', scale: 1.2, scaleStep: 0.005, minScale: 1.1, maxScale: 1.25 },
                        { arcAngle: 85, angle: -85, angleStep: -0.2, minAngle: 60, maxAngle: 170, rgb: '255, 0, 60', scale: 0.95, scaleStep: 0.005, minScale: 0.9, maxScale: 1.1 },
                        { arcAngle: 60, angle: -10, angleStep: -0.2, minAngle: 5, maxAngle: 90, rgb: '255, 0, 60', scale: 0.92, scaleStep: 0.005, minScale: 0.85, maxScale: 1.0 },
                        { arcAngle: 90, angle: -90, angleStep: -0.2, minAngle: 80, maxAngle: 180, rgb: '255, 155, 0', scale: 0.55, scaleStep: 0.005, minScale: 0.45, maxScale: 0.6 },
                        { arcAngle: 95, angle: 0, angleStep: -0.2, minAngle: -10, maxAngle: 100, rgb: '255, 155, 0', scale: 0.4, scaleStep: 0.005, minScale: 0.35, maxScale: 0.5 },
                        { arcAngle: 50, angle: -110, angleStep: -0.2, minAngle: 90, maxAngle: 170, rgb: '255, 155, 0', scale: 0.7, scaleStep: 0.005, minScale: 0.6, maxScale: 0.75 },
                        { arcAngle: 90, angle: -12, angleStep: -0.2, minAngle: 0, maxAngle: 130, rgb: '255, 155, 0', scale: 0.75, scaleStep: 0.005, minScale: 0.7, maxScale: 0.8 },
                        { arcAngle: 80, angle: -50, angleStep: -0.25, minAngle: 25, maxAngle: 145, rgb: '255, 255, 0', scale: 0.32, scaleStep: 0.005, minScale: 0.3, maxScale: 0.4 },
                        { arcAngle: 90, angle: -90, angleStep: -0.005, minAngle: 80, maxAngle: 200, rgb: '255, 255, 0', scale: 0.2, scaleStep: 0.005, minScale: 0.2, maxScale: 0.3 },
                        { arcAngle: 30, angle: -22, angleStep: -0.005, minAngle: 15, maxAngle: 80, rgb: '255, 255, 0', scale: 0.28, scaleStep: 0.005, minScale: 0.2, maxScale: 0.3 }
                    ],
                    //level 4
                    [
                        { arcAngle: 32, angle: -90, angleStep: -0.4, minAngle: 80, maxAngle: 140, rgb: '255, 0, 60', scale: 1.8, scaleStep: 0.005, minScale: 1.7, maxScale: 1.85 },
                        { arcAngle: 88, angle: -55, angleStep: -0.4, minAngle: 30, maxAngle: 160, rgb: '255, 0, 60', scale: 1.5, scaleStep: 0.005, minScale: 1.4, maxScale: 1.6 },
                        { arcAngle: 60, angle: 0, angleStep: -0.4, minAngle: -5, maxAngle: 90, rgb: '255, 0, 60', scale: 1.2, scaleStep: 0.005, minScale: 1.1, maxScale: 1.3 },
                        { arcAngle: 90, angle: -90, angleStep: -0.4, minAngle: 80, maxAngle: 190, rgb: '255, 0, 60', scale: 1.3, scaleStep: 0.005, minScale: 1.2, maxScale: 1.4 },
                        { arcAngle: 90, angle: 0, angleStep: -0.4, minAngle: 0, maxAngle: 120, rgb: '255, 155, 0', scale: 0.7, scaleStep: 0.005, minScale: 0.7, maxScale: 0.8 },
                        { arcAngle: 90, angle: -90, angleStep: -0.4, minAngle: -80, maxAngle: 185, rgb: '255, 155, 0', scale: 0.55, scaleStep: 0.005, minScale: 0.5, maxScale: 0.6 },
                        { arcAngle: 60, angle: 0, angleStep: -0.5, minAngle: 0, maxAngle: 100, rgb: '255, 155, 0', scale: 0.9, scaleStep: 0.005, minScale: 0.8, maxScale: 1 },
                        { arcAngle: 85, angle: -75, angleStep: -0.4, minAngle: 65, maxAngle: 170, rgb: '255, 155, 0', scale: 1, scaleStep: 0.005, minScale: 0.9, maxScale: 1.1 },
                        { arcAngle: 80, angle: -40, angleStep: -0.5, minAngle: 30, maxAngle: 155, rgb: '255, 255, 0', scale: 0.45, scaleStep: 0.005, minScale: 0.4, maxScale: 0.5 },
                        { arcAngle: 90, angle: 0, angleStep: -0.2, minAngle: -5, maxAngle: 120, rgb: '255, 255, 0', scale: 0.3, scaleStep: 0.005, minScale: 0.25, maxScale: 0.35 },
                        { arcAngle: 30, angle: -120, angleStep: -0.2, minAngle: 100, maxAngle: 170, rgb: '255, 255, 0', scale: 0.35, scaleStep: 0.005, minScale: 0.3, maxScale: 0.4 }
                    ],
                ];
    };
    
    initShapes();

    // update();
    // 
    // drawShapes(shapes, level);
    
    setInterval(function() {
        update();
        ctx.clearRect(0, 0, w, h);
        drawShapes(shapes, level);
    }, 1000 / 30);
};