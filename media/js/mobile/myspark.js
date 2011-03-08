var initSpark = function (level) {
	var canvas = document.getElementById('spark'),
	    ctx = canvas.getContext("2d"),
	    h = 200,
		w = $('#wrapper').width(),
		shapes = [],
    	ignorelist = [];

    if(level === 1) {
      ignorelist = [1, 3, 4, 5, 7, 9 ];
    }

    if(level === 2) {
      ignorelist = [1, 4, 7, 9];
    }

    if(level === 3) {
      ignorelist = [4, 7];
    }

    if(level === 4) {
      ignorelist = [7];  
    }

    if(level === 5) {
      ignorelist = [];
    }


    window.onorientationchange = function() {
        w = $('#wrapper').width();
        canvas.width = w;
    }

    $(window).resize(function() {
        w = $('#wrapper').width();
        canvas.width = w;
        console.log('resize');
    });

    canvas.height = h;
    canvas.width = w;

	function deg2rad(degrees) {
		return degrees * Math.PI/180;
	}

	function drawShapes(shapes, posx, posy, level) {
        
        var multiplier = 1 + (level / 10);
        
        for(i = 0, nb = shapes.length; i < nb; i += 1) {
            var shape = shapes[i];

            if(ignorelist.indexOf(i) === -1) {
             	ctx.save();
    		    	ctx.fillStyle = "rgba("+shape.rgb+", 0.6)";
    		    	if (window.innerHeight > window.innerWidth) {
    	  		        ctx.translate((w/2) + (posx * shape.moveFactor), (h - 30) + (posy * shape.moveFactor));
    		    	} else {
    		    	    ctx.translate((w/2) + (posx * shape.moveFactor), (h - 30));
    		    	};
    		        ctx.rotate(deg2rad(shape.angle));
    		        ctx.beginPath();
    		        ctx.moveTo(0, 0);
    		        ctx.arc(0, 0, 100 * multiplier * shape.scale, 0, -deg2rad(shape.arcAngle), true);
    		        ctx.fill();
    		    ctx.restore();
    		}
        }
	}

	function update() {
        for(var i = 0, nb = shapes.length; i < nb; i += 1) {
            var s = shapes[i];
            
            s.moveFactor = 1-(i/6);
            
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

    var initShapes = function() {
        shapes = [ { arcAngle: 100, angle: -90, angleStep: -0.1, minAngle: 80, maxAngle: 190, rgb: '255, 0, 60', scale: 0.95, scaleStep: 0.01, minScale: 0.8, maxScale: 0.95 },
                    { arcAngle: 35, angle: -100, angleStep: -0.3, minAngle: 70, maxAngle: 160, rgb: '255, 0, 60', scale: 1.1, scaleStep: 0.015, minScale: 0.9, maxScale: 1.1 },
                    { arcAngle: 120, angle: -0, angleStep: -0.3, minAngle: 180, maxAngle: -20, rgb: '255, 0, 60', scale: 1, scaleStep: 0.01, minScale: 0.95, maxScale: 1 },
                    { arcAngle: 155, angle: -10, angleStep: -0.5, minAngle: -30, maxAngle: 170, rgb: '255, 0, 60', scale: 0.9, scaleStep: 0.02, minScale: 0.65, maxScale: 0.9 },
                    { arcAngle: 45, angle: -77, angleStep: -2, minAngle: 50, maxAngle: 120, rgb: '255, 155, 0', scale: 0.7, scaleStep: 0.01, minScale: 0.5, maxScale: 0.7 },
                    { arcAngle: 65, angle: -95, angleStep: -1.5, minAngle: 80, maxAngle: 200, rgb: '255, 155, 0', scale: 0.6, scaleStep: 0.018, minScale: 0.5, maxScale: 0.6 },
                    { arcAngle: 95, angle: 0, angleStep: -2, minAngle: -5, maxAngle: 110, rgb: '255, 155, 0', scale: 0.7, scaleStep: 0.015, minScale: 0.65, maxScale: 0.85 },
                    { arcAngle: 45, angle: -45, angleStep: -1.1, minAngle: 40, maxAngle: 140, rgb: '255, 155, 0', scale: 0.75, scaleStep: 0.01, minScale: 0.55, maxScale: 0.75 },
                    { arcAngle: 55, angle: -90, angleStep: -0.9, minAngle: 90, maxAngle: 170, rgb: '255, 255, 0', scale: 0.55, scaleStep: 0.01, minScale: 0.4, maxScale: 0.65 },
                    { arcAngle: 35, angle: -120, angleStep: -1.2, minAngle: 100, maxAngle: 180, rgb: '255, 255, 0', scale: 0.4, scaleStep: 0.015, minScale: 0.3, maxScale: 0.5 },
                    { arcAngle: 30, angle: -40, angleStep: -1.3, minAngle: 15, maxAngle: 75, rgb: '255, 255, 0', scale: 0.4, scaleStep: 0.018, minScale: 0.3, maxScale: 0.5 },
                    { arcAngle: 90, angle: -0, angleStep: -0.005, minAngle: 0, maxAngle: 95, rgb: '255, 255, 0', scale: 0.25, scaleStep: 0.02, minScale: 0.15, maxScale: 0.25 } 
                    ];
    };
    
    // Parallax

	function initMove() {
        window.addEventListener("MozOrientation", setPosition, true);
	}

	var posx = 0;
	var posy = 0;

	function setPosition(o) {
	    if(window.innerHeight > window.innerWidth) {
	     	posx = o.x * 100;
			posy = (o.y - 0.6) * 100;
	    } else {
	        posy = (o.x - 0.6) * -100;
			posx = o.y * -100;
	    }
	}
	
	initShapes();
    initMove();

    setInterval(function() {
        update();
        ctx.clearRect(0, 0, w, h);
        drawShapes(shapes, posx, posy, level);
    }, 1000 / 50);
}