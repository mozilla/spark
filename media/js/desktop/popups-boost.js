var initBoost = function() {
    // Open the correct Boost popup
    $('#user-details .popup-trigger').click(function() {
        var status = parseInt($('#boost').data('status'));
        if(status === 0) {
            $('#boost').show();
        } else if(status === 1) {
            $('#boost2').show();
        }
        showPopup();
    });
    
    // Let's boost button
    $('#boost .right-button').click(function() {
        swap('#boost', '#boost1');
    });
    
    // Try again (boost 1)
    $('#location-error .right-button').click(function() {
        swap('#boost1-confirm', '#boost1');
    });
    
    // Manual geolocation form
    popupForm('#select-location-form', null, function($form, resp) {
        refreshYourLocation(resp.data.cityName, resp.data.countryName);
        swap('#select-location', '#boost1-confirm');
        $('#location-error').hide();
        $('#location-result').show();
    });
    
    // Select your location manually
    $('#location-error .cta a').click(function(e) {
        $.get($(this).attr('href'), function(cities) {
            var citylist = $("#select-location-form-citylist");

            //¨Populate city drop-down
            $.each(cities, function(index, city) {
                citylist.append($("<option />").val(city[0]).text(city[1]));
            });
            
            swap('#boost1-confirm', '#select-location');
        });
        e.preventDefault();
        return false;
    });
    
    // Boost 1 Confirm
    popupForm('#boost1-confirm-form', null, function($form, resp) {
        if(resp.status === 'success') {
            $.get(resp.url, function(html) {
                $('#user-location').html(html);
                $('#user-location-link').hide();
            });
            swap('#boost1-confirm', '#boost2');
        }
    });
    
    // Boost 1 Confirm - Cancel button
    $('#location-result .left-button').click(function(e) {
        $('#select-location-form-citylist').val('0');
        swap('#boost1-confirm', '#select-location');
    });
    
    // Boost 2 form
    popupForm('#boost2-form', null, function($form, resp) {
        if(resp.data.parent) {
            $('#parent-name').html(resp.data.parent);
            $('#has-parent').val(resp.data.parent);
            $('#boost2-result-parent').show();
            $('#boost2-result-solo').hide();
        } else {
            $('#no-parent').val('1');
            $('#boost2-result-parent').hide();
            $('#boost2-result-solo').show();
        }
        
        swap('#boost2', '#boost2-confirm');
    });
    
    // Boost 2 - Maybe Later button
    $('#boost2 .left-button').click(function(e) {
        resetForm('#boost2-form');
    });
    
    // Boost 2 Complete form
    popupForm('#boost2-confirm-form', null, function($form, resp) {
        if(resp.status === 'success') {
            $.get(resp.url, function(html) {
                $('#parent-user').html(html);
                $('#parent-user-link').hide();
            });
            hidePopup();
        }
    });
    
    // Boost 2 Complete - Cancel button
    $('#boost2-confirm-form .left-button').click(function(e) {
        resetForm('#boost2-form');
        swap('#boost2-confirm', '#boost2');
    });
    
    /*
    var boost1Error = function() {
        alert('error');
    };
    var boost1Success = function() {
        alert('success');
    };
    popupForm('#boost1-form', boost1Error, boost1Success);*/
};

var geoSuccess = function() {
    swap('#boost1', '#boost1-confirm');
    refreshYourLocation($('#city').val(), $('#country').val());
    $('#location-error').hide();
    $('#location-result').show();
};

var geoError = function() {
    swap('#boost1', '#boost1-confirm');
    $('#location-error').show();
    $('#location-result').hide();
};

var onLocateClick = function() {
    $('#geolocate a').hide();
	$('#geolocate img').show();
	$('ul.errorlist').hide();
};

var initBoostPopups = function() {
    initBoost();
    initGeolocation(onLocateClick, geoSuccess, geoError);
};


// Helper functions

var refreshYourLocation = function(city, country) {
    $('#your-location').find('span').html(city+', '+country);
};

