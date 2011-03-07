	var canvas = document.getElementById('spark'),
	    ctx = canvas.getContext("2d"),
	    h = 200,
		w = $('#wrapper').width(),
		shapes = [];

    canvas.height = h;
    canvas.width = w;

	function deg2rad(degrees) {
		return degrees * Math.PI/180;
	}

    function createShape(shape) {
        shapes.push(shape);
    }

	function drawShapes(shapes, multiplier) {                    
        
        if(multiplier < 1) {
            //shapes.splice(6);
        }
        
        for(i = 0, nb = shapes.length; i < nb; i += 1) {
            var shape = shapes[i];

         	ctx.save();
		    	ctx.fillStyle = "rgba("+shape.rgb+", 0.6)";
		        ctx.translate(w/2, h - 30);
		        ctx.rotate(deg2rad(shape.angle));
		        ctx.beginPath();
		        ctx.moveTo(0, 0);
		        ctx.arc(0, 0, 100 * multiplier * shape.scale, 0, -deg2rad(shape.arcAngle), true);
		        ctx.fill();
		    ctx.restore();
        }
	}

	function update() {
        for(var i = 0, nb = shapes.length; i < nb; i += 1) {
            var s = shapes[i];
            
            if(Math.abs(s.angle) > (s.maxAngle - s.arcAngle) || Math.abs(s.angle) < s.minAngle) {
                s.angleStep *= -1;
            } 
            s.angle += s.angleStep;
            
            if(s.scale > s.maxScale || s.scale < s.minScale) {
                s.scaleStep *= -1;
            }
            s.scale += s.scaleStep;
        }
	}

    function initShapes(multiplier) {
        if(multiplier < 1) {
            createShape({ arcAngle: 100, angle: -80, angleStep: -0.1, minAngle: 80, maxAngle: 190, rgb: '255, 0, 60', scale: 0.85, scaleStep: 0.01, minScale: 0.8, maxScale: 0.95 });
            createShape({ arcAngle: 35, angle: -120, angleStep: -0.3, minAngle: 70, maxAngle: 160, rgb: '255, 0, 60', scale: 0.95, scaleStep: 0.015, minScale: 0.9, maxScale: 1.1 });
            createShape({ arcAngle: 155, angle: -10, angleStep: -0.5, minAngle: -30, maxAngle: 170, rgb: '255, 0, 60', scale: 0.8, scaleStep: 0.02, minScale: 0.65, maxScale: 0.9 });
            createShape({ arcAngle: 45, angle: -77, angleStep: -2, minAngle: 50, maxAngle: 120, rgb: '255, 255, 0', scale: 0.6, scaleStep: 0.01, minScale: 0.5, maxScale: 0.7 });
            createShape({ arcAngle: 95, angle: -15, angleStep: -1, minAngle: 10, maxAngle: 170, rgb: '255, 155, 0', scale: 0.75, scaleStep: 0.02, minScale: 0.65, maxScale: 0.85 });
            createShape({ arcAngle: 45, angle: -45, angleStep: -1, minAngle: 40, maxAngle: 140, rgb: '255, 155, 0', scale: 0.6, scaleStep: 0.01, minScale: 0.55, maxScale: 0.75 });        
        } else {
            if (multiplier < 1.3) {
                createShape({ arcAngle: 100, angle: -80, angleStep: -0.1, minAngle: 80, maxAngle: 190, rgb: '255, 0, 60', scale: 0.85, scaleStep: 0.01, minScale: 0.8, maxScale: 0.95 });
                createShape({ arcAngle: 35, angle: -120, angleStep: -0.3, minAngle: 70, maxAngle: 160, rgb: '255, 0, 60', scale: 0.95, scaleStep: 0.015, minScale: 0.9, maxScale: 1.1 });
                createShape({ arcAngle: 155, angle: -10, angleStep: -0.5, minAngle: -30, maxAngle: 170, rgb: '255, 0, 60', scale: 0.8, scaleStep: 0.02, minScale: 0.65, maxScale: 0.9 });
                createShape({ arcAngle: 45, angle: -77, angleStep: -2, minAngle: 50, maxAngle: 120, rgb: '255, 255, 0', scale: 0.6, scaleStep: 0.01, minScale: 0.5, maxScale: 0.7 });
                createShape({ arcAngle: 95, angle: -15, angleStep: -1, minAngle: 10, maxAngle: 170, rgb: '255, 155, 0', scale: 0.75, scaleStep: 0.02, minScale: 0.65, maxScale: 0.85 });
                createShape({ arcAngle: 45, angle: -45, angleStep: -1, minAngle: 40, maxAngle: 140, rgb: '255, 155, 0', scale: 0.6, scaleStep: 0.01, minScale: 0.55, maxScale: 0.75 });
                createShape({ arcAngle: 45, angle: -90, angleStep: -1, minAngle: 90, maxAngle: 170, rgb: '255, 255, 0', scale: 0.5, scaleStep: 0.01, minScale: 0.4, maxScale: 0.65 });
                createShape({ arcAngle: 45, angle: -120, angleStep: -1, minAngle: 100, maxAngle: 180, rgb: '255, 255, 0', scale: 0.4, scaleStep: 0.015, minScale: 0.3, maxScale: 0.5 });
                createShape({ arcAngle: 90, angle: -0, angleStep: -0.005, minAngle: 0, maxAngle: 95, rgb: '255, 255, 0', scale: 0.2, scaleStep: 0.01, minScale: 0.15, maxScale: 0.25 });
                createShape({ arcAngle: 45, angle: -45, angleStep: -1, minAngle: 40, maxAngle: 140, rgb: '255, 155, 0', scale: 0.6, scaleStep: 0.01, minScale: 0.55, maxScale: 0.75 });
            } else {
                createShape({ arcAngle: 100, angle: -80, angleStep: -0.1, minAngle: 80, maxAngle: 190, rgb: '255, 0, 60', scale: 0.85, scaleStep: 0.01, minScale: 0.8, maxScale: 0.95 });
                createShape({ arcAngle: 35, angle: -120, angleStep: -0.3, minAngle: 70, maxAngle: 160, rgb: '255, 0, 60', scale: 0.95, scaleStep: 0.015, minScale: 0.9, maxScale: 1.1 });
                createShape({ arcAngle: 55, angle: -100, angleStep: -0.2, minAngle: 40, maxAngle: 140, rgb: '255, 0, 60', scale: 1, scaleStep: 0.02, minScale: 0.75, maxScale: 1 });
                createShape({ arcAngle: 155, angle: -10, angleStep: -0.5, minAngle: -30, maxAngle: 170, rgb: '255, 0, 60', scale: 0.8, scaleStep: 0.02, minScale: 0.65, maxScale: 0.9 });
                createShape({ arcAngle: 45, angle: -77, angleStep: -2, minAngle: 50, maxAngle: 120, rgb: '255, 255, 0', scale: 0.6, scaleStep: 0.01, minScale: 0.5, maxScale: 0.7 });
                createShape({ arcAngle: 95, angle: -15, angleStep: -1, minAngle: 10, maxAngle: 170, rgb: '255, 155, 0', scale: 0.75, scaleStep: 0.02, minScale: 0.65, maxScale: 0.85 });
                createShape({ arcAngle: 80, angle: -25, angleStep: -0.8, minAngle: 25, maxAngle: 155, rgb: '255, 155, 0', scale: 0.7, scaleStep: 0.015, minScale: 0.6, maxScale: 0.80 });
                createShape({ arcAngle: 45, angle: -45, angleStep: -1, minAngle: 40, maxAngle: 140, rgb: '255, 155, 0', scale: 0.6, scaleStep: 0.01, minScale: 0.55, maxScale: 0.75 });
                createShape({ arcAngle: 45, angle: -90, angleStep: -1, minAngle: 90, maxAngle: 170, rgb: '255, 255, 0', scale: 0.5, scaleStep: 0.01, minScale: 0.4, maxScale: 0.65 });
                createShape({ arcAngle: 45, angle: -120, angleStep: -1, minAngle: 100, maxAngle: 180, rgb: '255, 255, 0', scale: 0.4, scaleStep: 0.015, minScale: 0.3, maxScale: 0.5 });
                createShape({ arcAngle: 45, angle: -92, angleStep: -1.1, minAngle: 120, maxAngle: 180, rgb: '255, 255, 0', scale: 0.3, scaleStep: 0.025, minScale: 0.2, maxScale: 0.4 });
                createShape({ arcAngle: 90, angle: -0, angleStep: -0.005, minAngle: 0, maxAngle: 95, rgb: '255, 255, 0', scale: 0.2, scaleStep: 0.01, minScale: 0.15, maxScale: 0.25 });
                createShape({ arcAngle: 45, angle: -45, angleStep: -1, minAngle: 40, maxAngle: 140, rgb: '255, 155, 0', scale: 0.6, scaleStep: 0.01, minScale: 0.55, maxScale: 0.75 });
            };
        };   
    }