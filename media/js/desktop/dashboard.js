var countUp = function(totalSeconds) {
    var $days = $('#days span.count'),
        $hours = $('#hours span.count'),
        $minutes = $('#minutes span.count'),
        $seconds = $('#seconds span.count');

    var pad = function(number, length) {
        var str = '' + number;

        while (str.length < length) {
            str = '0' + str;
        }

        return str;
    };

    var timeToString = function(dd, hh, mm, ss) {
        $days.text(pad(dd, 2) + ' :');
        $hours.text(pad(hh, 2) + ' :');
        $minutes.text(pad(mm, 2) + ' :');
        $seconds.text(pad(ss, 2));
    };

    var processTime = function(total) {
        var dd = Math.floor(total / 86400),
            ddRemainder = total % 86400,
            hh = Math.floor(ddRemainder / 3600),
            hhRemainder = ddRemainder % 3600,
            mm = Math.floor(hhRemainder / 60),
            mmRemainder = hhRemainder % 60,
            ss = mmRemainder % 60;

        timeToString(dd, hh, mm, ss);
    };

    var updateTime = function() {
        processTime(totalSeconds);
        setInterval(function() {
           totalSeconds += 1;

           processTime(totalSeconds);
        }, 1000);
    };

    updateTime();
};

var initSpark = function (level) {
    var canvas = document.getElementById('spark'),
        ctx = canvas.getContext("2d"),
        h = $('#spark-graphic').height(),
    	w = $('#spark-graphic').width(),
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

    canvas.height = h;
    canvas.width = w;

    var deg2rad = function(degrees) {
    	return degrees * Math.PI/180;
    };

    var rand = function(min, max) {
        return min + Math.floor(Math.random() * (max - min));
    };

    var drawShapes = function(shapes, level) {

        var multiplier = 1 + (level / 10);

        for(i = 0, nb = shapes.length; i < nb; i += 1) {
            var shape = shapes[i];
            
            if(ignorelist.indexOf(i) === -1) {
             	ctx.save();
                    ctx.shadowBlur = 30;
                    ctx.shadowColor = "rgba(0,0,0,0.2)";
        	    	ctx.fillStyle = "rgba("+shape.rgb+", 0.6)";
        		    ctx.translate(w / 2, h);
        	        ctx.rotate(deg2rad(shape.angle));
        	        ctx.beginPath();
        	        ctx.moveTo(0, 0);
        	        ctx.arc(0, 0, 100 * multiplier * shape.scale, 0, -deg2rad(shape.arcAngle), true);
        	        ctx.fill();
        	    ctx.restore();
            }
        }
    };

    var update = function() {
        for(var i = 0, nb = shapes.length; i < nb; i += 1) {
            var s = shapes[i];

            s.moveFactor = 1-(i/6);

            if(Math.abs(s.angle) > (s.maxAngle - s.arcAngle) || Math.abs(s.angle) < s.minAngle) {
                s.angleStep *= -1;
            } 
            s.angle += s.angleStep * rand(1, 2);

            if(s.scale > s.maxScale || s.scale < s.minScale) {
                s.scaleStep *= -1;
            }
            s.scale += s.scaleStep * rand(1, 2);
        }
    };

    var initShapes = function() {
        shapes = [ { arcAngle: 100, angle: -90, angleStep: -0.1, minAngle: 80, maxAngle: 190, rgb: '255, 0, 60', scale: 0.95, scaleStep: 0.01, minScale: 0.8, maxScale: 0.95 },
                    { arcAngle: 35, angle: -100, angleStep: -0.3, minAngle: 70, maxAngle: 160, rgb: '255, 0, 60', scale: 1.1, scaleStep: 0.015, minScale: 0.9, maxScale: 1.1 },
                    { arcAngle: 120, angle: -0, angleStep: -0.3, minAngle: 180, maxAngle: -20, rgb: '255, 0, 60', scale: 1, scaleStep: 0.01, minScale: 0.95, maxScale: 1 },
                    { arcAngle: 155, angle: -10, angleStep: -0.5, minAngle: -30, maxAngle: 170, rgb: '255, 0, 60', scale: 0.9, scaleStep: 0.02, minScale: 0.65, maxScale: 0.9 },
                    { arcAngle: 45, angle: -77, angleStep: -1, minAngle: 50, maxAngle: 120, rgb: '255, 155, 0', scale: 0.7, scaleStep: 0.01, minScale: 0.5, maxScale: 0.7 },
                    { arcAngle: 65, angle: -95, angleStep: -0.8, minAngle: 80, maxAngle: 200, rgb: '255, 155, 0', scale: 0.6, scaleStep: 0.018, minScale: 0.5, maxScale: 0.6 },
                    { arcAngle: 95, angle: 0, angleStep: -1, minAngle: -5, maxAngle: 110, rgb: '255, 155, 0', scale: 0.7, scaleStep: 0.015, minScale: 0.65, maxScale: 0.85 },
                    { arcAngle: 45, angle: -45, angleStep: -0.6, minAngle: 40, maxAngle: 140, rgb: '255, 155, 0', scale: 0.75, scaleStep: 0.01, minScale: 0.55, maxScale: 0.75 },
                    { arcAngle: 55, angle: -90, angleStep: -0.7, minAngle: 90, maxAngle: 170, rgb: '255, 255, 0', scale: 0.55, scaleStep: 0.01, minScale: 0.4, maxScale: 0.65 },
                    { arcAngle: 35, angle: -120, angleStep: -0.8, minAngle: 100, maxAngle: 180, rgb: '255, 255, 0', scale: 0.4, scaleStep: 0.015, minScale: 0.3, maxScale: 0.5 },
                    { arcAngle: 30, angle: -40, angleStep: -0.9, minAngle: 15, maxAngle: 75, rgb: '255, 255, 0', scale: 0.4, scaleStep: 0.018, minScale: 0.3, maxScale: 0.5 },
                    { arcAngle: 90, angle: -0, angleStep: -0.005, minAngle: 0, maxAngle: 95, rgb: '255, 255, 0', scale: 0.25, scaleStep: 0.02, minScale: 0.15, maxScale: 0.25 } 
                    ];
    };
    
    initShapes();

    update();
    
    drawShapes(shapes, level);
    
    // setInterval(function() {
    //     update();
    //     ctx.clearRect(0, 0, w, h);
    //     drawShapes(shapes, level);
    // }, 1000 / 30);
};

// Countries you've reached
var initSparkedCountries = function(countryList) {
    var R = Raphael("minimap", 310, 174),
        countries = getCountries(R),
        style = {fill: '#ffd40d', 'stroke-width': 0};

    for(var c in countries) {
        countries[c].attr(style).hide();
    }

    var list = countryList;

    for(var i=0, max=list.length; i < max; i += 1) {
        var cc = list[i];
        countries[cc].show();
    }   
};

// Countries tooltip
var $tooltip = $('#tooltip');

$(document).mousemove(function(e){
    var w = $tooltip.width(); 

   $tooltip.css({
       'left' : e.pageX - ((w / 2) + 15),
       'top' : e.pageY + 27
    });
});

$('#minimap').hover(function() {
    $tooltip.toggle();
}, function() {
    $tooltip.toggle();
});