var x = 972798180000,
    y = 973798180000,
    d1 = new Date(x),
    d2 = new Date(y),
    delta = 0,
    deltaStep = (y - x) / MAXVALUE,
    yy1 = d1.getFullYear().toString().slice(2),
    mm1 = d1.getMonth() + 1,
    dd1 = d1.getDate(),
    hh1 = d1.getHours(),
    min1 = d1.getMinutes(),
    ss1 = d1.getSeconds(),
    yy2 = d2.getFullYear().toString().slice(2),
    mm2 = d2.getMonth() + 1,
    dd2 = d2.getDate(),
    hh2 = d2.getHours(),
    min2 = d2.getMinutes(),
    ss2 = d2.getSeconds();

var pad = function(number, length) {
    var str = '' + number;

    while (str.length < length) {
        str = '0' + str;
    }

    return str;
};

$('#start-date').text(pad(mm1, 2) + "." + pad(dd1, 2) + "." + yy1 + " " + pad(hh1, 2) + ":" + pad(min1, 2) + ":" + pad(ss1, 2));
$('#current-date').text(pad(mm2, 2) + "." + pad(dd2, 2) + "." + yy2 + " " + pad(hh2, 2) + ":" + pad(min2, 2) + ":" + pad(ss2, 2));

var updateDelta = function(x, value) {
    delta = deltaStep * value;

    var d3 = new Date(x + delta),
        yy3 = d3.getFullYear().toString().slice(2),
        mm3 = d3.getMonth() + 1,
        dd3 = d3.getDate(),
        hh3 = d3.getHours(),
        min3 = d3.getMinutes(),
        ss3 = d3.getSeconds();

    $time.text(pad(mm3, 2) + "." + pad(dd3, 2) + "." + yy3 + " " + pad(hh3, 2) + ":" + pad(min3, 2) + ":" + pad(ss3, 2));
};