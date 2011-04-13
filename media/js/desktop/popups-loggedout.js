var success = function($form, data) {
    $form.find('button').attr("disabled", "disabled");
    
    if($form[0].id === 'signup') {
        $.cookie('new_user', '1', {expires: 3, path:'/'});
    }
    
    setTimeout(function() {
        // Redirect to logged-in user home page
        window.location.replace(data.next);
    }, 200);
};

function initLoginForm() {
    $('#forgot-password').click(function() {
       swap('#sign-in', '#password-recovery');
    });

    $('#login .close').click(function() {
        resetForm('#login');
    });
    
    var error = function(fieldname) {
        if(fieldname === 'all') {
            resetField('#login-password input');
        }
    };

    popupForm('#login', error, success);
}

function initRegisterForm() {
    $('#signup .close').click(function() {
        resetForm('#signup');
    });
    
    var error = function(fieldname) {
        if(fieldname === 'all') {
            resetField('#register-password input');
            resetField('#register-confirm-password input');
        }
    };

    popupForm('#signup', error, success);
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
    initRegisterForm();
    initPasswordRecoverForm();
});