function initLoginForm() {
    $('#forgot-password').click(function() {
       swap('#sign-in', '#password-recovery');
    });
    
    $('#sign-in p.download a').click(function() {
       hidePopup();
    });
    
    $('#login .close').click(function() {
        resetForm('#login');
    });
    
    var error = function(fieldname) {
        if(fieldname === 'all') {
            resetField('#login-password input');
        }
    };
    
    var success = function($form, data) {
        $form.find('button').attr("disabled", "disabled");
        setTimeout(function() {
            // Redirect to logged-in user home page
            window.location.replace(data.next);
        }, 200);
    };
    
    popupForm('#login', error, success);
}

function initPasswordRecoverForm() {
    $('#password-recovery .left-button').click(function() {
        resetForm('#recover');
        swap('#password-recovery', '#sign-in');
    });
    
    var success = function(data) {
        resetForm('#recover');
        swap('#password-recovery', '#success');
    };
    
    popupForm('#recover', null, success);
}

$(document).ready(function() {
    initPlaceholders();
    initLoginForm();
    initPasswordRecoverForm();
});