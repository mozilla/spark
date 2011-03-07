function initLoginForm() {
    $('#forgot-password').click(function() {
       $('#sign-in').fadeOut(150);
       $('#password-recovery').delay(160).fadeIn(150);
    });
    
    $('#sign-in p.download a').click(function() {
       hidePopup(); 
    });
    
    $('#login .close').click(function() {
        $('#login').resetFormAfter(150);
    });
    
    popupForm('login', function(fieldname) {
        if(fieldname === 'all') {
            $('#login-password input').resetAfter(0);
        }
    }, function($form, data) {
        $form.find('button').attr("disabled", "disabled");
        setTimeout(function() {
            window.location.replace(data.next);
        }, 200);
    });
}

function initPasswordRecoverForm() {
    $('#password-recovery .left-button').click(function() {
        $('#recover').resetFormAfter(150);
        $('#password-recovery').fadeOut(150);
        $('#sign-in').delay(160).fadeIn(150);
    });
    
    popupForm('recover', function() {}, function(data) {
        $('#recover').resetFormAfter(150);
        $('#password-recovery').fadeOut(150);
        $('#success').delay(160).fadeIn(150);
    });
}

$(document).ready(function() {
    initPlaceholders();
    initLoginForm();
    initPasswordRecoverForm();
});