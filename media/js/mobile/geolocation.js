$(document).ready(function() {
    var timer = null;
    
	var process = function(info) {
		if(info.coords) {
		    $('#lat').attr('value', info.coords.latitude);
		    $('#long').attr('value', info.coords.longitude);
		}
		if(info.address) {
		    $('#city').attr('value', info.address.city);
		    $('#country-code').attr('value', info.address.countryCode);
		    $('#country').attr('value', info.address.country);
		}
		$('form').submit();
	}
	
	var error = function() {
	    $('form').submit();
	}
	
	var geolocateMe = function() {
    	navigator.geolocation.getCurrentPosition(process, error, {timeout: 8000});
    	
    	$('#geolocate a').hide();
    	$('#geolocate img').show();
    };
    
    $('#geolocate').click(geolocateMe);
});