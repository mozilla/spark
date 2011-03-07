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


function initPlaceholders() {
    var $inputs = $('input[placeholder]');

    if (!Modernizr.input.placeholder) {
        $inputs.addClass('placeholder');
    }

    $inputs.addPlaceholder();
    $('span.placeholder').click(function() {
        $(this).prev('input').focus();
    });

    $inputs.focus(function() {
       $(this).next('span.placeholder').hide();
    });
}