$(document).ready(function() {
    popupForm('login', function(fieldname) {
        if(fieldname === 'all') {
            $('#login-password input').val('').trigger('focusout');
        }
    });
    
	var $inputs = $('input[placeholder]');

    if (!Modernizr.input.placeholder){
        $inputs.addClass('placeholder');
    }

	$inputs.addPlaceholder(); 
    $('span.placeholder').click(function() {
        $(this).prev('input').focus();
    })
    
    $inputs.focus(function() {
       $(this).next('span.placeholder').hide(); 
    });
    
});

var popupForm = function(formId, errorCallback) {
    var $form = $('#'+formId),
        $submitButton = $form.find('button'),
    
        beforeForm = function() {
        	//$submitButton.attr("disabled", "disabled");
        	$('.errorlist').remove();
        },

        showError = function(msg) {
            $form.find('fieldset').prepend('<ul class="errorlist"><li>'+msg+'</li></ul>');
        },

        showFieldError = function(fieldname, msg) {
            var $fieldWrapper = $('#'+formId+'-'+fieldname);
            $fieldWrapper.after('<ul class="errorlist"><li>'+msg+'</li></ul>');
            $fieldWrapper.find('input').addClass('error');
        },

        processResponse = function(data) {
            if (data) {
        		if(data.status === 'error') {
        			$.each(data.errors, function(fieldname, errmsg) {
        			    if(fieldname === '__all__') {
        			        showError(errmsg[0]);
        			        errorCallback('all');
        			    } else {
            		        showFieldError(fieldname, errmsg[0]);
            		        errorCallback(fieldname);
        			    }
        			});

		            $submitButton.removeAttr("disabled");
        		} else if(data.status === 'success') {
        		    setTimeout(function() {
                        window.location.replace(data.next);
                    }, 200);
        		}
            }
        };

    options = {
        dataType: 'json',
        success: processResponse,
        beforeSubmit: beforeForm
    };
    
    $form.ajaxForm(options);
};

// placeholder fallback script
var testinput = document.createElement('input');
	$.extend($.support, { placeholder: !!('placeholder' in testinput) });

	$.fn.addPlaceholder = function(options){
		var settings = {
			'class': 'placeholder',
			'allowspaces': false,
			'dopass': true,
			'dotextarea': true,
			'checkafill': true
		};

		return this.each(function(){
			if ($.support.placeholder) return false;

			$.extend( settings, options );

			if ( !( this.tagName=='INPUT' || (settings['dotextarea'] && this.tagName=='TEXTAREA') ) ) return true;

			var $this = $(this),
				ph = this.getAttribute('placeholder'),
				ispass = $this.is('input[type=password]');

			if (!ph) return true;

			if (settings['dopass'] && ispass) {
				passPlacehold($this, ph);
			}
			else if (!ispass) {
				inputPlacehold($this, ph)
			}
		});

		function inputPlacehold(el, ph) {
			if ( valueEmpty(el.val()) ) {
				el.val(ph);
				el.addClass(settings['class']);
			}

			el.focusin(function(){
				if (el.hasClass(settings['class'])) {
					el.removeClass(settings['class']);
					el.val('');
				}
			});
			el.focusout(function(){
				if ( valueEmpty(el.val()) ) {
					el.val(ph);
					el.addClass(settings['class']);
				}
			});
		}

		function passPlacehold(el, ph) {
			el.addClass(settings['class']);
			var span = $('<span/>',{
				'class': el.attr('class')+' '+settings['class'],
				text: ph,
				css: {
					border:		'none',
					cursor:		'text',
					background:	'transparent',
					position:	'absolute',
					top:		el.position().top,
					left:		el.position().left,
					lineHeight: el.height()+20+'px',
					paddingLeft:parseFloat(el.css('paddingLeft'))+1+'px'
				}
			}).insertAfter(el);

			el.focusin(function(){
				if (el.hasClass(settings['class'])) {
					span.hide();
					el.removeClass(settings['class']);
				}
			});
			el.focusout(function(){
				if ( valueEmpty(el.val()) ) {
					span.show();
					el.addClass(settings['class']);
				}
			});

			if (settings['checkafill']) {
				(function checkPass(){
					if (!valueEmpty(el.val()) && el.hasClass(settings['class'])) {
						el.focusin();
					}
					setTimeout(checkPass, 250);
				})();
			}
		}

		function valueEmpty( value ) {
			return settings['allowspaces'] ? value==='' : $.trim(value)==='';
		}
	};

