var height = 770,
    width = $('#wrapper').width(),
    r = Raphael('visualization', width, height),
    zpd = new RaphaelZPD(r, { zoom: true, pan: true, drag: false }, $('#content')[0]);

var random = function(min, max) {
    return min + Math.floor(Math.random() * (max - min));
};

r.customAttributes.arc = function(x, y, dx, dy, radius) {
    var path = [["M", x, y], ["A", radius, radius, 0, 1, 1, dx, dy]];
    return { path: path };
};

var createArc = function(posCity1, posCity2, stroke, hue, opacity, city1, city2) {
    var style = {"stroke": "hsla(" + hue + ", 100, 55, 1)", "stroke-width": stroke, "stroke-linecap": "butt", "stroke-opacity": opacity};
    
    var node = r.path().attr(style).attr({arc: [posCity1, 650, posCity2, 650, 1] }).node;
    node.id = city1 + ":" + city2;
    currentStrokes[node.id] = stroke;
};

var createHalfCircle = function(posCity, hue, opacity, city, radius) {
    var style = {"stroke": 0, "fill": "hsla(" + hue + ", 100, 55, "+ opacity + ")", "stroke-linecap": "butt"};
    
    radius /= 2;
    halfCircles[city] = r.path().attr(style);
    currentRadii[city] = radius;
};

var initCityList = function() {
    var textStyle = {
        "text-align": "left",
        "text-anchor": "start",
        "alignment-baseline": "topline",
        "font-family": "arial",
        "font-size": "2px",
        "fill": "#fff"
    };

    var x = 0,
        y = 0,
        textOffset = 5;
        citylist = r.set();

    for(var i = 0; i < nbCities; i += 1) {
        var x = i * (width / (nbCities));
        var y = height - (height - 650) + textOffset;
        
        citylist.push(r.text(x, y, cities[i]).attr(textStyle).rotate(90, x, y));
    }
    
    var style = {"fill": "rgba(0,0,0,0.01)", "stroke": "none"};
    var node = r.rect(0, 650, width, 40).attr(style).node;
    node.id = "boundingBox";
    
    var textGroup = r.group(0, citylist);
};

var initShapes = function() {
    for(var i = 0; i < nbNodes; i += 1) {
        var city1 = finalShares[i][0],
            city2 = finalShares[i][1],
            nbShares = finalShares[i][2],
            posCity1 = (city1 - 1) * (width / nbCities),
            posCity2 = (city2 - 1) * (width / nbCities),
            stroke = 0,
            opacity = 0.3,
            hue;

        if((city2 - city1) <= (nbCities * 0.8)) {
            hue = 60 - (((1 / (nbCities * 0.8)) * (city2 - city1) * 55));
        } else {
            hue = Math.floor((city2 - city1) - 60);
        };

        if(posCity1 != posCity2) {
             createArc(posCity1, posCity2, stroke, hue, opacity, city1, city2);
        } else {
            createHalfCircle(posCity1, hue, opacity, city1, stroke);
        }
    }
};