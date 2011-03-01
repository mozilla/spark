$(document).ready(function() {
    var $zoom = $('#zoom'),
        $timelapse = $('#time-wrapper'),
        windowHeight,
        windowWidth,
        currentScale,
        currentTime,
        isPlaying = false,
        wasPlaying = false;

    // Gets the current value of the time slider
    var updateCurrentTime = function() {
        currentTime = $timelapse.slider("value");
    };

    // Increments the value of the time slider
    var updateTimelapse = function() {
        $timelapse.slider('value', currentTime + 1)
    }

    // Plays/pauses the timelapse replay
    var togglePlay = function() {
        isPlaying = !isPlaying;

        if(isPlaying) {
            playTimelapse = setInterval(function() {
                updateCurrentTime();
                updateTimelapse();
            }, 30);
        } else {
            clearInterval(playTimelapse);
        }
        $('#play').toggle();
        $('#pause').toggle();
    };

    // Sets the dimensions of the mask
    var initMask = function() {
        windowHeight = $(document).height();
        windowWidth = $(window).width();
        
        $('#mask').css({'width' : windowWidth, 'height' : windowHeight});   
    }

    // Gets the current value of the zoom slider
    var updateCurrentScale = function() {
        currentScale = $zoom.slider("value");
    };

    // Updates the position of the tooltip
    $(document).mousemove(function(e){
       $('#tooltip').css({
           'left' : e.pageX - 87,
           'top' : e.pageY + 27
        });
    });

    // Creates the time slider
	$('#time-wrapper').slider({
		range: "min",
		min: 0,
		max: 600,
		step: 1
	});

    // Creates the zoom slider
    $zoom.slider({
		min: 0,
		max: 3,
		step: 1
	});

    // Makes the current time label move with the slider handle
    $('#time-wrapper').bind('slidechange', function() {
       var x = $('#time-wrapper a').css('left');

       $('#current-time').css({'left' : x}); 
    });
    
    // Increases the value of the zoom slider
    $('#zoom-in').click(function() {

        updateCurrentScale();
        $zoom.slider("value", (currentScale + 1));
    });
    
    // Decreases the value of the zoom slider
    $('#zoom-out').click(function() {
        
        updateCurrentScale();
        $zoom.slider("value", (currentScale - 1));
    });

    // Toggles hightlight on magnifier icons depending on the current value
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

    // Shows the sign-in modal popup
    $('#sign-in').click(function() {
       $('#mask').fadeIn(200);
       $('#sign-in-window').fadeIn(200);
    });

    // Hides the sign-in modal popup
    $('#mask').click(function() {
       $(this).fadeOut(200);
       $('#sign-in-window').fadeOut(200);
    });

    // Sets negative margins to the modal popup in order to center it on screen
    $('#sign-in-window').css( {
        'marginLeft' : -(($('#sign-in-window').width() + 52)/2),
        'marginTop' : -(($('#sign-in-window').height() + 42)/2)
    });
    
    // Triggers the play/pause and toggles the corresponding strings
    $('#play').click(function() { 
        togglePlay();
    });
    $('#pause').click(function() { 
        togglePlay();
    });
    
    // Stops playing when the slider is manually changed
    $('#time-wrapper').mousedown(function() {
        if(isPlaying) {
            togglePlay();
            wasPlaying = !wasPlaying;
            $('#loading').fadeIn(100);
        }
    });
    
    // Resumes playing when slider is released, but only if this happens after interrupting replay
    $('body').mouseup(function() {
        if(wasPlaying) {
            togglePlay();
            wasPlaying = !wasPlaying;
            $('#loading').fadeOut(100);
        }
    });
            
    // Resizes the mask when the window is resized to avoid scrollbars
    $(window).resize(function() {
        initMask();  
    });
    
    initMask();
});