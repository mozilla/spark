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

var $tooltip = $('#tooltip'),
    $tooltipContent = $('#tooltip span');

// Countries you've reached
var initSparkedCountries = function(countryList) {
    var R = Raphael("minimap", 310, 174),
        countries = getCountries(R),
        style = {fill: '#ffd40d', 'stroke-width': 0};

    for(var c in countries) {
        countries[c].attr(style).hide();
        countries[c].hover((function(code) {
            return function() {
                $tooltip.show();
                // India cc must be appended with a _ not to be confused
                // with the JavaScript 'in' operator which generates errors
                // during JS compression.
                code = code === 'in_' ? 'in':code;
                $tooltipContent.text(countryNames[code]);   
            }
        })(c),
        function() {
            $tooltip.hide();
        });
    }

    var list = countryList;

    for(var i=0, max=list.length; i < max; i += 1) {
        var cc = list[i];
        cc = cc === 'in' ? 'in_' : cc;

        countries[cc].show();
    }
};

// Countries tooltip
$(document).mousemove(function(e){
    var w = $tooltip.width(); 

   $tooltip.css({
       'left' : e.pageX - ((w / 2) + 10),
       'top' : e.pageY + 27
    });
});
