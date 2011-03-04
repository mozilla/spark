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
        
        $('#password-confirm').fadeOut(150);
        $('#password-complete').delay(160).fadeIn(150);
    }

    // Code to execute to display the Reset Popup
    $('#password-complete').hide();
    showResetPopup();

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

    // triggers password-recovery when forgot-password link is clicked
    $('#forgot-password').click(function() {
       $('#sign-in').fadeOut(150);
       $('#password-recovery').delay(160).fadeIn(150);
    });
    
    // displays success if previous form is filled
    // DELETE THIS ONCE THE FORM WORKS
    $('#password-recovery a.left-button').click(function() {
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

    // account popup close button
    $('#popup a.close').click(function() {
       hidePopup(); 
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

    // Slider
    var container = $('div#list-container');
    var ul = $('#random-stats');

    var itemsWidth = ul.innerWidth() - container.outerWidth();

    $('#slider').slider({
        min: 0,
        max: itemsWidth,
        handle: '#handle',
        // stop: function (event, ui) {
        //     ul.animate({'left' : ui.value * -1}, 500);
        // },
        slide: function (event, ui) {
           ul.css('left', ui.value * -1);
        }
    });

    // Execute functions below

    initMask();

    // Resizes the mask when the window is resized to avoird scrollbars
    $(window).resize(function() {
        initMask();  
    });
});