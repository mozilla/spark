var initBoost = function() {
    // Let's boost
    $('#boost .right-button').click(function() {
        swap('#boost', '#boost1');
    });
    
    // Try again (boost 1)
    $('#location-error .right-button').click(function() {
        swap('#boost1-confirm', '#boost1');
    });
    

    popupForm('#select-location-form', null, function($form, data) {
        refreshYourLocation(data.cityName, data.countryName);
        swap('#select-location', '#boost1-confirm');
    });
    
    // Select your location manually
    $('#location-error .cta a').click(function(e) {
        $.get($(this).attr('href'), function(cities) {
            var citylist = $("#citylist");

            //¨Populate city drop-down
            $.each(cities, function(index, city) {
                citylist.append($("<option />").val(city[0]).text(city[1]));
            });
            
            swap('#boost1-confirm', '#select-location');
        });
        e.preventDefault();
        return false;
    });

    // Next step (boost 1 confirm)
    $('#boost1-confirm .right-button').click(function() {
        swap('#boost1-confirm', '#boost2');
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

