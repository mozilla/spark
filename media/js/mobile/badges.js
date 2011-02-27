var initBadges = function() {    
    var $badgelist = $('ul#badge-list'),
        $badges = $('ul#badge-list li'),
        viewportWidth,
        viewportHeight,
        portraitMargin,
        landscapeMargin,
        $badgeInfo,
        currentBadgeIndex = 0,
        currentBadgeElement = null,
        supportsOrientationChange = "onorientationchange" in window,
        orientationEvent = supportsOrientationChange ? "orientationchange" : "resize";

    var nbBadgesPerRow = function() {
        return viewportHeight > viewportWidth ? 3 : 5;
    };

    var positionBadgeArrow = function(badgeIndex, nbBadgesPerRow) {
        var badgePosition = ((badgeIndex - 1) % nbBadgesPerRow) + 1;

        if(viewportHeight > viewportWidth) {
            $('#badge-label img').css('left', 40 * badgePosition + ((portraitMargin + 40) * (badgePosition - 1)));
        } else {
            $('#badge-label img').css('left', 40 * badgePosition + ((landscapeMargin + 40) * (badgePosition - 1)));
        }
    };

    var showBadgeInfo = function(i) {
        var nb = nbBadgesPerRow(),
            count = $('ul#badge-list').data("count"),
            rowIndex = Math.ceil(i / nb),
            lastBadgeIndex = (rowIndex * nb) > count ? count : (rowIndex * nb),
            $lastBadge = $('li.badge[data-index="' + lastBadgeIndex + '"]');

        if(currentBadgeElement) {
            currentBadgeElement.className += " current";
        }
        
        $badgeInfo = $('#badge-label-tmpl').clone();
        $badgeInfo.attr('id', 'badge-label');
        $badgeInfo.find('h2').text("This is badge #"+i);
        $badgeInfo.find('p').text("In hac habitasse platea dictumst. Nam pulv inar, odio sed rhoncus suscipit, sem diam ultrices maurism lorem.");
        
        if(viewportHeight > viewportWidth) {
            $lastBadge.after($badgeInfo.css('marginLeft', portraitMargin).fadeIn(500));
        } else {
            $lastBadge.after($badgeInfo.css('marginLeft', landscapeMargin).fadeIn(500));
        }
        positionBadgeArrow(i, nb);
    };

    var hideBadgeInfo = function() {
        if($badgeInfo) {
            $badgeInfo.fadeOut(2000).remove();
        };
    };
            
    var positionBadges = function() {
        var w;

        viewportWidth = document.documentElement.clientWidth;
        viewportHeight = document.documentElement.clientHeight;
        w = viewportWidth - 32;
        portraitMargin = (w - 256) / 2;
        landscapeMargin = (w - 416) / 4;
        
        if(viewportHeight > viewportWidth) {
            $badgelist.css('marginLeft', -portraitMargin);
            $badges.css('marginLeft', portraitMargin);
        } else {
            $badgelist.css('marginLeft', -landscapeMargin);
            $badges.css('marginLeft', landscapeMargin);
        }
        
        if(currentBadgeIndex > 0) {
            hideBadgeInfo();
            showBadgeInfo(currentBadgeIndex);
        }
    };
    
    $('#badge-list li').click(function() {
        var i = $(this).data('index');

        currentBadgeElement = this;

        $('li.badge.current').removeClass('current');
        if($('#badge-label').length > 0 || i !== currentBadgeIndex) {
            hideBadgeInfo();
            if(i !== currentBadgeIndex) {
                showBadgeInfo(i);
            }
        }
        else {
            showBadgeInfo(i);
        }
        
        currentBadgeIndex = i;
    });
    
    positionBadges();
    
    window.addEventListener(orientationEvent, positionBadges, false);
};