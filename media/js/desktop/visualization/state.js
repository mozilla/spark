var DURATION = 30,
    MINVALUE = 0,
    MAXVALUE = 3000,
    GRANULARITY = 10,
    STROKEFACTOR = 12,
    RADIUSFACTOR = 1.5,
    MINSHARES = 0,
    nbCities,
    nbNodes,
    nbSteps,
    arcs = {},
    halfCircles = {},
    currentStrokes = {},
    currentRadii = {},
    currentAnimations = [],
    currentScale,
    currentTime,
    isPlaying = false,
    focusedCity = -1;

var initState = function() {
    nbCities = cities.length;
    nbNodes = finalShares.length;
    nbSteps = shareHistory.length;
};

// gets the current value of the time slider
var updateCurrentTime = function() {
    currentTime = $timelapse.slider("value");
};

// gets the current value of the zoom slider
var updateCurrentScale = function() {
    currentScale = $zoom.slider("value");
};

var resetObjectValues = function(obj) {
    for(var key in obj) {
        obj[key] = 0;
    }
};

var resetHalfCircles = function() {
    for(id in halfCircles) {
        halfCircles[id].attr({arc: [0, 0, 0, 0, 1]});
    }
};

var resetArcs = function() {
    for(var key in currentStrokes) {
        var node = document.getElementById(key);
        node.style.strokeWidth = 0;
    }
};

var clearAll = function() {
    resetHalfCircles();
    resetArcs();
};

var refreshNodes = function() {
    var stroke,
        radius,
        xPos;

    clearAll();
    
    for(var key in currentStrokes) {
        if(currentStrokes[key] !== 0) {
            stroke = currentStrokes[key];
            var node = document.getElementById(key);
            node.style.strokeWidth = stroke;
        }
    }
    
    for(var key in currentRadii) {
        if(currentRadii[key] !== 0) {
            radius = currentRadii[key];
            xPos = key * (width / (nbCities - 1));
            
            halfCircles[key].attr({arc: [xPos - radius, 650, xPos + radius, 650, 1]})
        }
    }
};

var fastForward = function(currentTime) {
    clearAnimations();
    resetObjectValues(currentStrokes);
    resetObjectValues(currentRadii);
    
    var stepsToCurrentTime = Math.floor(currentTime / GRANULARITY);

    for (var i = 0; i < stepsToCurrentTime; i += 1) {
        var nbPairs = shareHistory[i].length;

        for(var j = 0; j < nbPairs; j += 1) {
            var city1 = shareHistory[i][j][0],
                city2 = shareHistory[i][j][1],
                nbShares = shareHistory[i][j][2],
                nodeId = city1 + ":" + city2,
                node = document.getElementById(nodeId),
                stroke = nbShares / STROKEFACTOR,
                radius = nbShares / RADIUSFACTOR;

            if(city1 === focusedCity || city2 === focusedCity || focusedCity === -1) {
                if(city1 === city2) {
                    if(nbShares >= MINSHARES) {
                        currentRadii[city1] = radius;   
                    }
                } else {
                    if(nbShares >= MINSHARES) {
                        currentStrokes[nodeId] = stroke;   
                    }
                }   
            }
        }
    }
    
    refreshNodes();
};

var togglePlay = function() {
    isPlaying = !isPlaying;
    
    if(isPlaying) {
        playTimelapse();
        showPauseButton();
    } else {
        stopTimelapse();
        showPlayButton();
    }
};

var drawFinalState = function() {
    fastForward(MAXVALUE);
};

var resetTimelapse = function() {
    $timelapse.slider('value', MINVALUE);
};

var resetToCurrentTime = function() {
    updateCurrentTime();
    fastForward(currentTime);
    if(!isPlaying && currentTime === MINVALUE) {
        fastForward(MAXVALUE);
    }
};