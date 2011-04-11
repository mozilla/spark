var initSpark = function (level) {
	var canvas = document.getElementById('spark'),
	    ctx = canvas.getContext("2d"),
	    h = 250,
		w = $('#wrapper').width(),
    	shapes = [],
    	smokeCircles = [],
    	colors = [];


    window.onorientationchange = function() {
        w = $('#wrapper').width();
        canvas.width = w;
    }

    $(window).resize(function() {
        w = $('#wrapper').width();
        canvas.width = w;
    });

    canvas.height = h;
    canvas.width = w;

	function deg2rad(degrees) {
		return degrees * Math.PI/180;
	}
	
	var rand = function(min, max) {
        return min + Math.floor(Math.random() * (max - min));
    };
    
    var randSpecial = function(min, max) {
        return min + (Math.random() * (max - min));
    };

	function drawShapes(shapes, posx, posy, level) {
        
        for(i = 0, nb = shapes[level - 1].length; i < nb; i += 1) {
            var shape = shapes[level - 1][i];
            
         	ctx.save();
		    	ctx.fillStyle = "rgba("+shape.rgb+", 0.6)";
		    	if (window.innerHeight > window.innerWidth) {
	  		        ctx.translate((w/2) - (posx * shape.moveFactor), (h - 30) - (posy * shape.moveFactor));
		    	} else {
		    	    ctx.translate((w/2) + (posx * shape.moveFactor), (h - 30));
		    	};
		        ctx.rotate(deg2rad(shape.angle));
		        ctx.beginPath();
		        ctx.moveTo(0, 0);
		        ctx.arc(0, 0, 100 * shape.scale, 0, -deg2rad(shape.arcAngle), true);
		        ctx.fill();
		    ctx.restore();
        }
	}

    var updateSpark = function() {
        var dice;
        for(var i = 0, nb = shapes[level - 1].length; i < nb; i += 1) {
            var s = shapes[level - 1][i],
                dice = rand(1, 30);
                
            s.moveFactor = 1-(i/6);
            
            if(Math.abs(s.angle) > (s.maxAngle - s.arcAngle) || Math.abs(s.angle) < s.minAngle || dice === 6) {
                s.angleStep *= -1;
            } 
            s.angle += s.angleStep * rand(1, 2);

            if(s.scale > s.maxScale || s.scale < s.minScale || dice === 4) {
                s.scaleStep *= -1;
            }
            
            s.scale += s.scaleStep * rand(1, 2);
        }
    };

    var initShapes = function() {
        var red = '237, 33, 37',
            orange = '255, 171, 13',
            yellow = '255, 255, 40';
        
        shapes = [ 
                    //level 1
                    [
                        { arcAngle: 80, angle: -20, angleStep: -0.2, minAngle: 20, maxAngle: 110, rgb: red, scale: 0.75, scaleStep: 0.005, minScale: 0.7, maxScale: 0.8 },
                        { arcAngle: 80, angle: -40, angleStep: -0.3, minAngle: -15, maxAngle: -50, rgb: red, scale: 0.65, scaleStep: 0.005, minScale: 0.6, maxScale: 0.7 },
                        { arcAngle: 80, angle: -65, angleStep: -0.2, minAngle: -40, maxAngle: -80, rgb: orange, scale: 0.55, scaleStep: 0.005, minScale: 0.5, maxScale: 0.6 },
                        { arcAngle: 95, angle: -2, angleStep: -0.2, minAngle: 0, maxAngle: -20, rgb: orange, scale: 0.45, scaleStep: 0.005, minScale: 0.4, maxScale: 0.5 },
                        { arcAngle: 105, angle: -55, angleStep: -0.25, minAngle: -50, maxAngle: -75, rgb: yellow, scale: 0.35, scaleStep: 0.005, minScale: 0.3, maxScale: 0.4 },
                        { arcAngle: 105, angle: -75, angleStep: -0.005, minAngle: -60, maxAngle: -100, rgb: yellow, scale: 0.25, scaleStep: 0.005, minScale: 0.2, maxScale: 0.3 }
                    ],
                    //level 2
                    [
                        { arcAngle: 85, angle: -60, angleStep: -0.2, minAngle: 45, maxAngle: 140, rgb: red, scale: 0.95, scaleStep: 0.005, minScale: 0.9, maxScale: 1 },
                        { arcAngle: 85, angle: -15, angleStep: -0.2, minAngle: 15, maxAngle: 110, rgb: red, scale: 0.85, scaleStep: 0.005, minScale: 0.8, maxScale: 0.9 },
                        { arcAngle: 80, angle: -50, angleStep: -0.2, minAngle: 35, maxAngle: 120, rgb: red, scale: 0.75, scaleStep: 0.005, minScale: 0.7, maxScale: 0.8 },
                        { arcAngle: 80, angle: -80, angleStep: -0.2, minAngle: 60, maxAngle: 150, rgb: orange, scale: 0.65, scaleStep: 0.005, minScale: 0.6, maxScale: 0.7 },
                        { arcAngle: 105, angle: -35, angleStep: -0.25, minAngle: 25, maxAngle: 145, rgb: yellow, scale: 0.45, scaleStep: 0.005, minScale: 0.4, maxScale: 0.5 },
                        { arcAngle: 95, angle: -2, angleStep: -0.2, minAngle: 0, maxAngle: -20, rgb: orange, scale: 0.55, scaleStep: 0.005, minScale: 0.5, maxScale: 0.6 },
                        { arcAngle: 105, angle: -75, angleStep: -0.005, minAngle: -60, maxAngle: -100, rgb: yellow, scale: 0.35, scaleStep: 0.005, minScale: 0.3, maxScale: 0.4 }
                    ],
                    //level 3
                    [
                        { arcAngle: 88, angle: -55, angleStep: -0.2, minAngle: 30, maxAngle: 160, rgb: red, scale: 1.2, scaleStep: 0.005, minScale: 1.1, maxScale: 1.25 },
                        { arcAngle: 85, angle: -85, angleStep: -0.2, minAngle: 60, maxAngle: 170, rgb: red, scale: 0.95, scaleStep: 0.005, minScale: 0.9, maxScale: 1.1 },
                        { arcAngle: 60, angle: -10, angleStep: -0.2, minAngle: 5, maxAngle: 90, rgb: red, scale: 0.92, scaleStep: 0.005, minScale: 0.85, maxScale: 1.0 },
                        { arcAngle: 90, angle: -90, angleStep: -0.2, minAngle: 80, maxAngle: 180, rgb: orange, scale: 0.55, scaleStep: 0.005, minScale: 0.45, maxScale: 0.6 },
                        { arcAngle: 95, angle: 0, angleStep: -0.2, minAngle: -10, maxAngle: 100, rgb: orange, scale: 0.4, scaleStep: 0.005, minScale: 0.35, maxScale: 0.5 },
                        { arcAngle: 50, angle: -110, angleStep: -0.2, minAngle: 90, maxAngle: 170, rgb: orange, scale: 0.7, scaleStep: 0.005, minScale: 0.6, maxScale: 0.75 },
                        { arcAngle: 90, angle: -12, angleStep: -0.2, minAngle: 0, maxAngle: 130, rgb: orange, scale: 0.75, scaleStep: 0.005, minScale: 0.7, maxScale: 0.8 },
                        { arcAngle: 80, angle: -50, angleStep: -0.25, minAngle: 25, maxAngle: 145, rgb: yellow, scale: 0.32, scaleStep: 0.005, minScale: 0.3, maxScale: 0.4 },
                        { arcAngle: 90, angle: -90, angleStep: -0.005, minAngle: 80, maxAngle: 200, rgb: yellow, scale: 0.2, scaleStep: 0.005, minScale: 0.2, maxScale: 0.3 },
                        { arcAngle: 30, angle: -22, angleStep: -0.005, minAngle: 15, maxAngle: 80, rgb: yellow, scale: 0.28, scaleStep: 0.005, minScale: 0.2, maxScale: 0.3 }
                    ],
                    //level 4
                    [
                        { arcAngle: 32, angle: -90, angleStep: -1, minAngle: 80, maxAngle: 140, rgb: red, scale: 1.8, scaleStep: 0.005, minScale: 1.7, maxScale: 1.85 },
                        { arcAngle: 88, angle: -55, angleStep: -1, minAngle: 30, maxAngle: 160, rgb: red, scale: 1.5, scaleStep: 0.005, minScale: 1.4, maxScale: 1.6 },
                        { arcAngle: 60, angle: 0, angleStep: -1, minAngle: -5, maxAngle: 120, rgb: red, scale: 1.2, scaleStep: 0.005, minScale: 1.1, maxScale: 1.3 },
                        { arcAngle: 90, angle: -90, angleStep: -1, minAngle: 80, maxAngle: 190, rgb: red, scale: 1.3, scaleStep: 0.005, minScale: 1.2, maxScale: 1.4 },
                        { arcAngle: 90, angle: 0, angleStep: -1, minAngle: 0, maxAngle: 120, rgb: orange, scale: 0.7, scaleStep: 0.005, minScale: 0.7, maxScale: 0.8 },
                        { arcAngle: 90, angle: -90, angleStep: -1, minAngle: -80, maxAngle: 185, rgb: orange, scale: 0.55, scaleStep: 0.005, minScale: 0.5, maxScale: 0.6 },
                        { arcAngle: 60, angle: 0, angleStep: -1.1, minAngle: 0, maxAngle: 100, rgb: orange, scale: 0.9, scaleStep: 0.005, minScale: 0.8, maxScale: 1 },
                        { arcAngle: 85, angle: -75, angleStep: -1, minAngle: 65, maxAngle: 170, rgb: orange, scale: 1, scaleStep: 0.005, minScale: 0.9, maxScale: 1.1 },
                        { arcAngle: 80, angle: -40, angleStep: -1.1, minAngle: 30, maxAngle: 155, rgb: yellow, scale: 0.45, scaleStep: 0.005, minScale: 0.4, maxScale: 0.5 },
                        { arcAngle: 90, angle: 0, angleStep: -0.8, minAngle: -5, maxAngle: 120, rgb: yellow, scale: 0.3, scaleStep: 0.005, minScale: 0.25, maxScale: 0.35 },
                        { arcAngle: 30, angle: -120, angleStep: -0.8, minAngle: 100, maxAngle: 170, rgb: yellow, scale: 0.35, scaleStep: 0.005, minScale: 0.3, maxScale: 0.4 }
                    ]
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
        updateSpark();
        ctx.clearRect(0, 0, w, h);
        drawShapes(shapes, posx, posy, level);
    }, 1000 / 50);
}