function popupForm(formId, errorCallback, successCallback) {
    var $form = $(formId),
        $submitButton = $form.find('button'),
    
        beforeForm = function() {
            $submitButton.attr("disabled", "disabled");
        	$('span.error').remove();
        	$('.error').removeClass('error');
        },
        
        showError = function(msg) {
            $form.find('fieldset').prepend('<span class="error">'+msg+'</span>');
            $form.find('.input-wrapper').each(function() {
                $(this).addClass('error');
            });
        },

        showFieldError = function(fieldname, msg) {
            var $fieldWrapper = $(formId+'-'+fieldname);
            $fieldWrapper.after('<span class="error">'+msg+'</span>');
            $fieldWrapper.addClass('error');
        },

        processResponse = function(data) {
            if (data) {
        		if(data.status === 'error') {
        			$.each(data.errors, function(fieldname, errmsg) {
        			    if(fieldname === '__all__') {
        			        showError(errmsg[0]);
        			        if(errorCallback) {
            			        errorCallback('all');
            			    }
        			    } else {
            		        showFieldError(fieldname, errmsg[0]);
            		        if(errorCallback) {
                		        errorCallback(fieldname);
                		    }
        			    }
        			});

		            $submitButton.removeAttr("disabled");
        		} else if(data.status === 'success') {
        		    if(successCallback) {
            		    successCallback($form, data);   
        		    }
        		}
            }
        };

    options = {
        dataType: 'json',
        success: processResponse,
        beforeSubmit: beforeForm
    };
    
    $form.ajaxForm(options);
}

$.fn.resetAfter = function(delay) {
    var self = this;
    setTimeout(function() {
        self.val('').trigger('focusout');
    }, delay);
	return this;
};

$.fn.resetFormAfter = function(delay) {
    var self = this;
    setTimeout(function() {
        self.find('input:not([type=hidden])').each(function() {
            $(this).val('').trigger('focusout');
        });
        self.find('span.error').remove();
        self.find('.error').removeClass('error');
    }, delay);
	return this;
};

function swap(fromId, toId) {
    $(fromId).fadeOut(150);
    $(toId).delay(160).fadeIn(150);
}

function resetForm(formId) {
    $(formId).resetFormAfter(150);
}

function resetField(fieldId) {
    $(fieldId).resetAfter(0);
}
