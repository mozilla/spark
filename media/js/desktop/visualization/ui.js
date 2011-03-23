var $zoom,
    $timelapse,
    $handle,
    $time,
    timerWidth,
    $tooltip,
    $city,
    $cityname,
    windowHeight,
    windowWidth
    list = document.getElementById("cities-list");


var initSliders = function() {
    // creates the time slider
    $timelapse.slider({
    	range: "min",
    	min: MINVALUE,
    	max: MAXVALUE,
    	step: 1
    });

    // creates the zoom slider
    $zoom.slider({
    	min: 0,
    	max: 3,
    	step: 1
    });   
};

// sets negative margins to the modal popup in order to center it on screen
var initPopup = function() {
    $('#sign-in-window').css( {
      'marginLeft' : -(($('#sign-in-window').width() + 52)/2),
      'marginTop' : -(($('#sign-in-window').height() + 42)/2)
    });   
};

// sets the dimensions of the mask
var initMask = function() {
    windowHeight = $(document).height();
    windowWidth = $(window).width();

    $('#mask').css({'width' : windowWidth, 'height' : windowHeight});   
};

var showYourSharesInfo = function() {
    $('#your-shares-info').show();
    toggleFocus();
};

var hideYourSharesInfo = function() {
    $('#your-shares-info').hide();
    toggleFocus();
};

var toggleFocusInfo = function(focus) {
    if(focus != -1) {
        $('#focus-info').show();  
    } else {
        $('#focus-info').hide();
    }  
};

var toggleFocus = function() {
    list.value = -1;
    focusedCity = -1;
    toggleFocusInfo(list.value);
    if(list.disabled) {
        list.disabled = false;
    } else {
        list.disabled = true;
    }
};

var initUI = function() {
    $zoom = $('#zoom');
    $timelapse = $('#time-wrapper');
    $handle = $('#time-wrapper a');
    $time = $('#current-time');
    timerWidth = $('#time-wrapper').width();
    $tooltip = $('#tooltip');
    $city = $('svg text');
    $cityname = $('#tooltip span');

    // increases the value of the zoom slider
    $('#zoom-in').click(function() {

        updateCurrentScale();
        $zoom.slider("value", (currentScale + 1));
    });

    // decreases the value of the zoom slider
    $('#zoom-out').click(function() {

        updateCurrentScale();
        $zoom.slider("value", (currentScale - 1));
    });

    $zoom.bind('slidechange', function(event, ui) {
       if(ui.value <= 3 && ui.value > 0) {
           $('#visualization').addClass('pannable');
       } else {
           if($('#visualization').hasClass('pannable')) {
               $('#visualization').removeClass('pannable');   
           }
       }
    });

    // displays the sign-in modal popup
    $('#sign-in').click(function() {
        $('#mask').fadeIn(200);
        $('#sign-in-window').fadeIn(200);
    });

    // toggles hightlight on magnifiers icons depending on the current value
    $('#zoom').bind("slidechange", function () {

        updateCurrentScale();

        if(currentScale > 0) {
            $('#zoom-out').removeClass('off');
        } else {
            $('#zoom-out').addClass('off');
        }

        if(currentScale > 2) {
            $('#zoom-in').addClass('off');
        } else {
            $('#zoom-in').removeClass('off');
        }
    });

    // hides the sign-in modal popup
    $('#mask').click(function() {
        $(this).fadeOut(200);
        $('#sign-in-window').fadeOut(200);
    });

    // triggers the play/pause and toggles the corresponding strings
    $('#play-pause').click(function() {
        togglePlay();
    });

    // Resizes the mask when the window is resized to avoird scrollbars
    $(window).resize(function() {
        initMask();  
    });

    var updateTimeLabel = function(currentTime) {
        $time.css('left', (currentTime / MAXVALUE) * timerWidth);
        updateDelta(x, currentTime);
    };

    // stops playing when the slider is manually changed
    $timelapse.mousedown(function() {
        if(isPlaying) {
            togglePlay();
            $('body').mouseup(function() {
                togglePlay();
                $('body').unbind('mouseup');
            });
        };
    });

    $timelapse.bind('slide', function(event, ui) {
        fastForward(ui.value);
        updateTimeLabel(ui.value);
    });

    // resumes playing when slider is released, but only if this happens after interrupting replay
    $('body').mouseup(function() {
        $(window).unbind('mousemove');
    });

    // updates the position of the tooltip
    $(document).mousemove(function(e){
        var w = $tooltip.width(); 
    
       $tooltip.css({
           'left' : e.pageX - ((w / 2) + 15),
           'top' : e.pageY + 27
        });
    });
    
    // shows the popup
    $('#boundingBox').hover(function() {
        $tooltip.show();
    }, function() {
        $tooltip.hide();
    });

    $('#viewport1 g').hover(function() {
        $tooltip.show();
    }, function() {
        $tooltip.hide();
    })

    // writes the name of the city in the tooltip
    $city.mouseenter(function() {
       var content = $(this).text();
       $cityname.text(content);
    });

    // makes the current time label move with the slider handle
    $timelapse.bind('slidechange', function(event, ui) {
        updateTimeLabel(ui.value);
    });

    //Make spacebar play/pause
    $(document).bind('keydown', function(e) {
        var code = (e.keyCode ? e.keyCode : e.which);
        if(code === 32) {
            togglePlay();
        }
    });

    $(document).bind('keypress', function(e) {
        var code = (e.keyCode ? e.keyCode : e.which);
        if(code === 32) {
            return false;
        }
    });
    
    $('#show-everyone').click(function() {
        hideYourSharesInfo();
        shareHistory = globalHistory;
        resetToCurrentTime();
        $(this).toggle();
        $('#show-your-shares').toggle();
    });
    
    $('#show-your-shares').click(function() {
        showYourSharesInfo();
        shareHistory = userHistory;
        resetToCurrentTime();
        $(this).toggle();
        $('#show-everyone').toggle();
    });
    
    $("#cities-list").change(function () {
        $("select option:selected").each(function () {
            focusedCity = parseInt($(this).val());
            $('#focus-info').text($(this).text());
        });
        resetToCurrentTime();
        toggleFocusInfo(focusedCity);
    });

    $('#show-everyone').hide();

    list.disabled = false;

    initPopup();
    initMask();
    initSliders();
};
 
// increments the value of the time slider
var updateTimelapse = function() {
    $timelapse.slider('value', currentTime + 1)
};

var resetTimelapse = function() {
    $timelapse.slider('value', 0);
};

var showPlayButton = function() {
    $('#play').show();
    $('#pause').hide();
};

var showPauseButton = function() {
    $('#play').hide();
    $('#pause').show();  
};

var disableSlider = function() {
    $timelapse.slider('disable');
    sliderEnabled = false;
};