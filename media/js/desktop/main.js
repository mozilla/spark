$(document).ready(function() {

    // Modal popup

    // sets the dimensions of the mask
    var initMask = function() {
        windowHeight = $(document).height();
        windowWidth = $(window).width();
    
        $('#mask').css({'width' : windowWidth, 'height' : windowHeight});
        $('#mask-noclick').css({'width' : windowWidth, 'height' : windowHeight});
    };

    var showPopup = function() {
        // sets negative margins to the modal popup in order to center it on screen
        $('#popup').css( {
            'marginLeft' : -(($('#popup').width() + 52)/2),
            'marginTop' : -(($('#popup').height() + 42)/2)
        });
        
        $('#mask').fadeIn(200);
        $('#popup').fadeIn(200);
    };

    var hidePopup = function() {
        $('#mask').fadeOut(200);
        $('#popup').fadeOut(200);
        setTimeout(function() {
            $('#popup').children().hide();
        }, 200)
    };

    var showResetPopup = function() {
        // sets negative margins to the modal popup in order to center it on screen
        $('#popup').css( {
            'marginLeft' : -(($('#popup').width() + 52)/2),
            'marginTop' : -(($('#popup').height() + 42)/2)
        });
        
        $('#mask-noclick').fadeIn(200);
        $('#popup').fadeIn(200);
    };

    var showResetComplete = function() {
        $('#popup').css( {
            'marginLeft' : -(($('#popup').width() + 52)/2),
            'marginTop' : -(($('#popup').height() + 42)/2)
        });
        
        $('#mask-noclick').hide();
        $('#mask').show();
        $('#password-confirm').fadeOut(150);
        $('#password-complete').delay(160).fadeIn(150);
    };

    var hideResetPopup = function() {
        $('#mask').fadeOut(200);
        $('#popup').fadeOut(200);
    };

    // Code to execute to display the Reset Popup
    // $('#password-complete').hide();
    // showResetPopup();

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
    $('#mask').click(function() {
        hidePopup();
    });

    // All elements with the class 'close' will close the popup when clicked
    $('#popup .close').click(function() {
       hidePopup(); 
    });

    // triggers password-recovery when forgot-password link is clicked
    $('#forgot-password').click(function() {
       $('#sign-in').fadeOut(150);
       $('#password-recovery').delay(160).fadeIn(150);
    });
    
    $('#sign-in p.download a').click(function() {
       hidePopup(); 
    });
    
    // goes back to sign in when start over button is clicked
    $('#password-recovery .left-button').click(function() {
       $('#password-recovery').fadeOut(150);
       $('#sign-in').delay(160).fadeIn(150); 
    });

    // test workflow 
    $('#password-recovery input').click(function() {
       $('#password-recovery').fadeOut(150);
       $('#success').delay(160).fadeIn(150); 
    });

    //Your account links
    //change password
    $('#your-account .change-password').click(function() {
       $('#your-account').fadeOut(150);
       $('#change-password').delay(160).fadeIn(150); 
    });

    //change email
    $('#your-account .change-email').click(function() {
       $('#your-account').fadeOut(150);
       $('#change-email').delay(160).fadeIn(150); 
    });

    //delete account
    $('#your-account .delete-account').click(function() {
       $('#your-account').fadeOut(150);
       $('#delete-account').delay(160).fadeIn(150); 
    });

    $('#change-password .left-button').click(function() {
       $('#change-password').fadeOut(150);
       $('#your-account').delay(160).fadeIn(150);
    });

    $('#change-email .left-button').click(function() {
       $('#change-email').fadeOut(150);
       $('#your-account').delay(160).fadeIn(150);
    });
    
    $('#delete-account .left-button').click(function() {
       $('#delete-account').fadeOut(150);
       $('#your-account').delay(160).fadeIn(150);
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

    $('#twitter').click(function() {
        var url = $(this).attr('href');
        
       tweetPopup(url);
       return false;
    });

    $('a.twitter').click(function() {
        var url = $(this).attr('href');
        
       tweetPopup(url);
       return false;
    });

    $('#facebook').click(function() {
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

    // Execute functions below

    initMask();

    // Resizes the mask when the window is resized to avoird scrollbars
    $(window).resize(function() {
        initMask();  
    });
});