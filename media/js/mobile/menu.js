var initMenu = function () {
    $('#menu-header').click(function() {
        if($(this).hasClass('closed')) {
            $(this).removeClass('closed').addClass('open');
            $('#menu').removeClass('closed').addClass('open');
            $('#menu-wrapper').removeClass('closed').addClass('open');
        } else {
            $(this).removeClass('open').addClass('closed');
            $('#menu').removeClass('open').addClass('closed');
            $('#menu-wrapper').removeClass('open').addClass('closed');
        }
        $('html').toggleClass('openmenu');
    });
    
    $('#logout').click(function() {
       $('#menu-content').fadeOut('fast');
       $('#logout-confirmation').fadeIn('fast');
    });
    
    $('#logout-confirmation .left-button').click(function() {
        $('#logout-confirmation').fadeOut('fast');
        $('#menu-content').fadeIn('fast');
    });
};

var hintMenu = function() {
    var $menu = $('#menu-wrapper'),
        docHeight = $(document).height();

    if(docHeight >= 500) {
        if($(window).scrollTop() === 0) {
            $menu.css('top', -55);
            setTimeout(function() {
                $menu.animate({'top': 0});
            }, 1000);
            $(window).scroll(function() {
                $menu.css('top', 0);
            });
        }
    } else {
        $menu.css('top', 0);
    }
};