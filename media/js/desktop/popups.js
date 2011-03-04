$(document).ready(function() {
    var $loginForm = $('#login-form'),
        $submitButton = $loginForm.find('button'),
        
        beforeForm = function() {
        	$submitButton.attr("disabled", "disabled");
        	$('.errorlist').remove();
        },
        
        showError = function(msg) {
            $loginForm.find('fieldset').prepend('<ul class="errorlist"><li>'+msg+'</li></ul>');
        },
        
        showFieldError = function(fieldname, msg) {
            $('#login-'+fieldname).after('<ul class="errorlist"><li>'+msg+'</li></ul>');
        },
        
        processResponse = function(data) {
            if (data) {
        		if(data.status === 'error') {
        			$.each(data.errors, function(fieldname, errmsg) {
        			    if(fieldname === '__all__') {
        			        showError(errmsg[0]);
        			    } else {
            		        showFieldError(fieldname, errmsg[0]);
        			    }
        			});
        			
		            $submitButton.removeAttr("disabled");
        		} else if(data.status === 'success') {
        		    setTimeout(function() {
                        window.location.replace(data.next);
                    }, 200);
        		}
            }
        },
        
        options = {
            dataType: 'json',
	        success: processResponse,
	        beforeSubmit: beforeForm
	    };
	
    $loginForm.ajaxForm(options);


    jQuery.fn.inputHints=function() {

        $(this).each(function(i) {
            $(this).val($(this).attr('placeholder'))
                .addClass('hint');
        });

        return $(this).focus(function() {
            if ($(this).val() == $(this).attr('placeholder'))
                $(this).val('')
                    .removeClass('hint');
        }).blur(function() {
            if ($(this).val() == '')
                $(this).val($(this).attr('placeholder'))
                    .addClass('hint');
        });
    };
    
    var $inputs = $('input[placeholder]');
    
    if (!Modernizr.input.placeholder){
        $inputs.inputHints();
    }
});