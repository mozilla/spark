function initGeolocation(clickCallback, successCallback, errorCallback) {
	var process = function(info) {
		if(info.coords) {
		    $('#lat').attr('value', info.coords.latitude);
		    $('#long').attr('value', info.coords.longitude);
		}
		if(info.address) {
		    $('#city').attr('value', info.address.city);
		    $('#country-code').attr('value', info.address.countryCode);
		    $('#country').attr('value', info.address.country);
		    if(info.address.countryCode === 'US' && info.address.postalCode) {
		        $('#us-state').attr('value', zipToState(info.address.postalCode));
		    }
		}
		if(successCallback) {
    		successCallback();
		}
	};
	
	var error = function() {
	    if(errorCallback) {
    	    errorCallback();
	    }
	};
    
    $('#geolocate').click(function() {
    	navigator.geolocation.getCurrentPosition(process, error, {timeout: 8000});
    	
    	if(clickCallback) {
    	    clickCallback();
    	}
    });
}

// Borrowed from http://zacharyburt.com/2010/02/javascript-zip-code-to-state-conversion/
function zipToState(zip) {
    var state;
	if (zip >= '99501' && zip <= '99950')  { state = 'AK'; }
	else if (zip >= '35004' && zip <= '36925')  { state = 'AL'; }
	else if (zip >= '71601' && zip <= '72959')  { state = 'AR'; }
	else if (zip >= '75502' && zip <= '75502')  { state = 'AR'; }
	else if (zip >= '85001' && zip <= '86556')  { state = 'AZ'; }
	else if (zip >= '90001' && zip <= '96162')  { state = 'CA'; }
	else if (zip >= '80001' && zip <= '81658')  { state = 'CO'; }
	else if (zip >= '06001' && zip <= '06389')  { state = 'CT'; }
	else if (zip >= '06401' && zip <= '06928')  { state = 'CT'; }
	else if (zip >= '20001' && zip <= '20039')  { state = 'DC'; }
	else if (zip >= '20042' && zip <= '20599')  { state = 'DC'; }
	else if (zip >= '20799' && zip <= '20799')  { state = 'DC'; }
	else if (zip >= '19701' && zip <= '19980')  { state = 'DE'; }
	else if (zip >= '32004' && zip <= '34997')  { state = 'FL'; }
	else if (zip >= '30001' && zip <= '31999')  { state = 'GA'; }
	else if (zip >= '39901' && zip <= '39901')  { state = 'GA'; }
	else if (zip >= '96701' && zip <= '96898')  { state = 'HI'; }
	else if (zip >= '50001' && zip <= '52809')  { state = 'IA'; }
	else if (zip >= '68119' && zip <= '68120')  { state = 'IA'; }
	else if (zip >= '83201' && zip <= '83876')  { state = 'ID'; }
	else if (zip >= '60001' && zip <= '62999')  { state = 'IL'; }
	else if (zip >= '46001' && zip <= '47997')  { state = 'IN'; }
	else if (zip >= '66002' && zip <= '67954')  { state = 'KS'; }
	else if (zip >= '40003' && zip <= '42788')  { state = 'KY'; }
	else if (zip >= '70001' && zip <= '71232')  { state = 'LA'; }
	else if (zip >= '71234' && zip <= '71497')  { state = 'LA'; }
	else if (zip >= '01001' && zip <= '02791')  { state = 'MA'; }
	else if (zip >= '05501' && zip <= '05544')  { state = 'MA'; }
	else if (zip >= '20331' && zip <= '20331')  { state = 'MD'; }
	else if (zip >= '20335' && zip <= '20797')  { state = 'MD'; }
	else if (zip >= '20812' && zip <= '21930')  { state = 'MD'; }
	else if (zip >= '03901' && zip <= '04992')  { state = 'ME'; }
	else if (zip >= '48001' && zip <= '49971')  { state = 'MI'; }
	else if (zip >= '55001' && zip <= '56763')  { state = 'MN'; }
	else if (zip >= '63001' && zip <= '65899')  { state = 'MO'; }
	else if (zip >= '38601' && zip <= '39776')  { state = 'MS'; }
	else if (zip >= '71233' && zip <= '71233')  { state = 'MS'; }
	else if (zip >= '59001' && zip <= '59937')  { state = 'MT'; }
	else if (zip >= '27006' && zip <= '28909')  { state = 'NC'; }
	else if (zip >= '58001' && zip <= '58856')  { state = 'ND'; }
	else if (zip >= '68001' && zip <= '68118')  { state = 'NE'; }
	else if (zip >= '68122' && zip <= '69367')  { state = 'NE'; }
	else if (zip >= '03031' && zip <= '03897')  { state = 'NH'; }
	else if (zip >= '07001' && zip <= '08989')  { state = 'NJ'; }
	else if (zip >= '87001' && zip <= '88441')  { state = 'NM'; }
	else if (zip >= '88901' && zip <= '89883')  { state = 'NV'; }
	else if (zip >= '06390' && zip <= '06390')  { state = 'NY'; }
	else if (zip >= '10001' && zip <= '14975')  { state = 'NY'; }
	else if (zip >= '43001' && zip <= '45999')  { state = 'OH'; }
	else if (zip >= '73001' && zip <= '73199')  { state = 'OK'; }
	else if (zip >= '73401' && zip <= '74966')  { state = 'OK'; }
	else if (zip >= '97001' && zip <= '97920')  { state = 'OR'; }
	else if (zip >= '15001' && zip <= '19640')  { state = 'PA'; }
	else if (zip >= '02801' && zip <= '02940')  { state = 'RI'; }
	else if (zip >= '29001' && zip <= '29948')  { state = 'SC'; }
	else if (zip >= '57001' && zip <= '57799')  { state = 'SD'; }
	else if (zip >= '37010' && zip <= '38589')  { state = 'TN'; }
	else if (zip >= '73301' && zip <= '73301')  { state = 'TX'; }
	else if (zip >= '75001' && zip <= '75501')  { state = 'TX'; }
	else if (zip >= '75503' && zip <= '79999')  { state = 'TX'; }
	else if (zip >= '88510' && zip <= '88589')  { state = 'TX'; }
	else if (zip >= '84001' && zip <= '84784')  { state = 'UT'; }
	else if (zip >= '20040' && zip <= '20041')  { state = 'VA'; }
	else if (zip >= '20040' && zip <= '20167')  { state = 'VA'; }
	else if (zip >= '20042' && zip <= '20042')  { state = 'VA'; }
	else if (zip >= '22001' && zip <= '24658')  { state = 'VA'; }
	else if (zip >= '05001' && zip <= '05495')  { state = 'VT'; }
	else if (zip >= '05601' && zip <= '05907')  { state = 'VT'; }
	else if (zip >= '98001' && zip <= '99403')  { state = 'WA'; }
	else if (zip >= '53001' && zip <= '54990')  { state = 'WI'; }
	else if (zip >= '24701' && zip <= '26886')  { state = 'WV'; }
	else if (zip >= '82001' && zip <= '83128')  { state = 'WY'; }
	return state;
}
