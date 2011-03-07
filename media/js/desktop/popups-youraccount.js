function initChangePasswordForm() {
    $('#change-password .left-button').click(function() {
        $('#changepw').resetFormAfter(150);
        $('#change-password').fadeOut(150);
        $('#your-account').delay(160).fadeIn(150);
    });
    
    popupForm('changepw');
}

function initChangeEmailForm() {
    $('#changeemail .left-button').click(function() {
        $('#changeemail').resetFormAfter(150);
        $('#change-email').fadeOut(150);
        $('#your-account').delay(160).fadeIn(150);
    });
    
    popupForm('changeemail', null, function(data) {
        var email = $('#changeemail-new_email input').val();
        $('#your-email span').text(email);
    });
}

function initDeleteAccountForm() {
    $('#change-password .left-button').click(function() {
        $('#changepw').resetFormAfter(150);
        $('#delete-account').fadeOut(150);
        $('#your-account').delay(160).fadeIn(150);
    });
    
    popupForm('delaccount');
}

$(document).ready(function() {
    initPlaceholders();
    initChangePasswordForm();
    initChangeEmailForm();
});