$(document).ready(function() {

// Modal popup

    // sets the dimensions of the mask
    var initMask = function() {
        windowHeight = $(document).height();
        windowWidth = $(window).width();
    
        $('#mask').css({'width' : windowWidth, 'height' : windowHeight});   
    }

    // displays the sign-in modal popup
    $('.popup-trigger').click(function() {
       $('#mask').fadeIn(200);
       $('#popup').fadeIn(200);
    });

    // hides the sign-in modal popup (and resets it to sign-in state)
    $('#mask').click(function() {
       $(this).fadeOut(200);
       $('#popup').fadeOut(200);
       setTimeout(function() {
           $('#password-recovery').hide();
           $('#password-sent').hide();
           $('#sign-in').show();
       }, 200)
    });

    // sets negative margins to the modal popup in order to center it on screen
    $('#popup').css( {
        'marginLeft' : -(($('#popup').width() + 52)/2),
        'marginTop' : -(($('#popup').height() + 42)/2)
    });

    // triggers password-recovery when forgot-password link is clicked
    $('#forgot-password').click(function() {
       $('#sign-in').fadeOut(150);
       $('#password-recovery').delay(151).fadeIn(150);
    });
    
    // displays password-sent if previous form is filled
    $('#password-recovery button.left-button').click(function() {
       $('#password-recovery').fadeOut(150);
       $('#password-sent').delay(151).fadeIn(150); 
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