var timelapseInterval;

var playTimelapse = function() {
        timelapseInterval = setInterval(function() {
        updateCurrentTime();
        updateTimelapse();

        if(currentTime === 1) {
            clearAll();
            resetObjectValues(currentStrokes);
            resetObjectValues(currentRadii);
        }
    
        if(currentTime % GRANULARITY === 0) {
            drawStep(currentTime / GRANULARITY);
        }
    
        if(currentTime === MAXVALUE) {
            stopTimelapse();
            showPlayButton();
            drawFinalState();
            resetTimelapse();
            isPlaying = false;
        }
    }, DURATION * 1000 / MAXVALUE );
};

var stopTimelapse = function() {
    clearInterval(timelapseInterval);
};

var animateArc = function(arc, stroke) {
    var counter = 0,
        oldStroke = arc.style.strokeWidth,
        strokeAnimation;

                
    // creates an animation between changes of size
    strokeAnimation = setInterval(function() {
        counter += 1;
        var s = oldStroke + ((stroke - oldStroke) / 10 * counter);

        arc.style.strokeWidth = s;
        if(counter === 10) {
            clearInterval(strokeAnimation);
        }
    }, DURATION * 1000 / MAXVALUE);
};

var animateCity = function(cityIndex, posCity, radius) {
    var counter = 0,
        animation;

    if(isPlaying && currentTime < MAXVALUE) {
            // creates an animation between changes of size
            animation = setInterval(function() {
                counter += 1;
                var oldRadius = currentRadii[cityIndex],
                    r = oldRadius + ((radius - oldRadius) / 10 * counter);
                    
                if(counter > 10) {
                    currentRadii[cityIndex] = radius;
                    clearInterval(animation);
                } else {
                    halfCircles[cityIndex].attr({arc: [posCity - r, 650, posCity + r, 650, 1]});
                }

            }, DURATION * 1000 / MAXVALUE);
            currentAnimations.push(animation);
    } else {
            // no animation
            halfCircles[cityIndex].attr({arc: [posCity - radius, 650, posCity + radius, 650, 1]});   
    }
};

var drawStep = function(s) {
    if(s > 0) {
        var step = shareHistory[s - 1],
            nbPairs = step.length;
            
        for(var i = 0; i < nbPairs; i += 1) {
            var city1 = step[i][0],
                city2 = step[i][1],
                posCity1 = (city1 - 1) * (width / nbCities),
                posCity2 = (city2 - 1) * (width / nbCities),
                nodeId = city1 + ":" + city2,
                node = document.getElementById(nodeId),
                nbShares = step[i][2],
                stroke = nbShares * strokeFactor,
                radius = nbShares * radiusFactor;
            
            if(city1 === focusedCity || city2 === focusedCity || focusedCity === -1) {
                if(city1 != city2) {
                    if(node.style.strokeWidth != stroke && nbShares >= MINSHARES) {
                       node.style.strokeWidth = stroke;
                       //animateArc(node, stroke);
                    }
                } else {
                    if(nbShares >= MINSHARES) {
                        animateCity(city1, posCity1, radius);
                    }
                }
            }
        }
    }
};

var clearAnimations = function() {
    for(var i = 0, nb = currentAnimations.length; i < nb; i += 1) {
        clearInterval(currentAnimations[i]);
    }
};