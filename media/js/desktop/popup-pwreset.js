function initPasswordResetForm() {
    var error = function(field) {
        if(field === 'all') {
            // Clear the values from both fields if passwords don't match
            $('#pwreset-new_password1 input').resetAfter(0);
            $('#pwreset-new_password2 input').resetAfter(0);    
        }
    };
    
    var success = function() {
        showResetComplete();
    }
    
    popupForm('pwreset', error, success);
}

$(document).ready(function() {
    initPlaceholders();
    initPasswordResetForm();
    
    $('#password-complete').hide();
    showResetPopup();
});