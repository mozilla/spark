// Modal popup
var $popup = $('#popup'),
    $mask = $('#mask'),
    $videoPlayer = $('#video-player'),
    video = document.querySelector('video');

// sets the dimensions of the mask
var initMask = function() {
    windowHeight = $(document).height();
    windowWidth = $(window).width();

    $mask.css({'width' : windowWidth, 'height' : windowHeight});
    $('#mask-noclick').css({'width' : windowWidth, 'height' : windowHeight});
};

var resizePopup = function() {
    $popup.css( {
        'marginLeft' : -(($popup.width() + 52)/2),
        'marginTop' : -(($popup.height() + 42)/2)
    });
};

var positionVideoPlayer = function() {
    $videoPlayer.css( {
        'marginLeft' : -(($videoPlayer.width() + 50) / 2),
        'marginTop' : -(($videoPlayer.height() + 50) / 2)
    });
};

var showPopup = function() {
    resizePopup();
    $mask.fadeIn(200);
    $popup.fadeIn(200);
};

var hideVideo = function() {
    $videoPlayer.fadeOut(200);
    video.pause();
};

var hidePopup = function() {
    $mask.fadeOut(200);
    $popup.fadeOut(200);
    if(video) {
        hideVideo();
    }
    setTimeout(function() {
        $popup.children().hide();
    }, 200)
};

var showResetPopup = function() {
    resizePopup();
    $('#mask-noclick').fadeIn(200);
    $popup.fadeIn(200);
};

var showResetComplete = function() {
    resizePopup();
    $('#mask-noclick').hide();
    $mask.show();
    $('#password-confirm').fadeOut(150);
    $('#password-complete').delay(160).fadeIn(150);
};

var hideResetPopup = function() {
    $mask.fadeOut(200);
    $popup.fadeOut(200);
};

var showVideoPlayer = function() {
    positionVideoPlayer();
    $mask.fadeIn(200);
    $videoPlayer.fadeIn(200);
};

$(document).ready(function() {
    // displays the sign-in modal popup
    $('.popup-trigger').click(function() {
        $('#sign-in').show();
        showPopup();
    });
    
    // displays the account manager popup
    $('#edit-account a').click(function() {
        $('#your-account').show();
        showPopup(); 
    });

    // hides the sign-in modal popup (and resets it to sign-in state)
    $mask.click(function() {
        hidePopup();
    });

    $('#video-player img').click(function() {
       hidePopup(); 
    });

    // All elements with the class 'close' will close the popup when clicked
    $('#popup .close').click(function() {
        hidePopup();
    });
    
    $('#password-confirm .close').click(function() {
        hideResetPopup();
        $('#mask-noclick').hide();
    });

    //opens video player
    $('a.video-launcher').click(function() {
       showVideoPlayer();
       video.play();
    });

    //Your account links
    //change password
    $('#your-account .change-password').click(function() {
       swap('#your-account', '#change-password');
    });

    //change email
    $('#your-account .change-email').click(function() {
       swap('#your-account', '#change-email');
    });

    //delete account
    $('#your-account .delete-account').click(function() {
       swap('#your-account', '#delete-account');
    });

    // popups
    
    function tweetPopup(url) {
        var h = $(window).height(),
            w = $(window).width(),
            top = (h / 2) - (450 / 2),
            left = (w / 2) - (550 / 2);

    	newwindow = window.open(url,'name','height=450,width=550,top='+top+',left='+left);
    	if (window.focus) {newwindow.focus()}
    }
    
    function fbPopup(url) {
        var h = $(window).height(),
            w = $(window).width(),
            top = (h / 2) - (400 / 2),
            left = (w / 2) - (580 / 2);

    	newwindow = window.open(url,'name','height=400,width=580,top='+top+',left='+left);
    	if (window.focus) {newwindow.focus()}
    }

    $('.twitter').click(function() {
        var url = $(this).attr('href');
        
       tweetPopup(url);
       return false;
    });

    $('a.twitter').click(function() {
        var url = $(this).attr('href');
        
       tweetPopup(url);
       return false;
    });

    $('.facebook').click(function() {
        var url = $(this).attr('href');
        
       fbPopup(url);
       return false;
    });

    // Smooth Scrolling
    $('a[href*=#]').click(function() {
        if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') 
            && location.hostname == this.hostname) {
                
            var $target = $(this.hash);
            $target = $target.length && $target || $('[name=' + this.hash.slice(1) +']');
            if ($target.length) {
                var targetOffset = $target.offset().top;
                $('html,body').animate({scrollTop: targetOffset}, 600);
                return false;
            }
        }
    });

    initMask();

    // Resizes the mask when the window is resized to avoird scrollbars
    $(window).resize(function() {
        initMask();  
    });
});