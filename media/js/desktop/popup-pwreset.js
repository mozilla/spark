function initPasswordResetForm() {
    var error = function(field) {
        if(field === 'all') {
            // Clear the values from both fields if passwords don't match
            resetField('#pwreset-new_password1 input');
            resetField('#pwreset-new_password2 input');
        }
    };
    
    var success = function() {
        showResetComplete();
    }
    
    popupForm('#pwreset', error, success);
}

$(document).ready(function() {
    initPlaceholders();
    initPasswordResetForm();
    
    $('#password-complete').hide();
    showResetPopup();
});