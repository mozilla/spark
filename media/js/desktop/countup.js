var countUp = function(totalSeconds) {
    var $days = $('#dd'),
        $hours = $('#hh'),
        $minutes = $('#mm'),
        $seconds = $('#ss');

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

    var processTime = function(totalSeconds) {
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

// replace totalSeconds by the actual value
countUp(totalSeconds);