function initChangePasswordForm() {
    $('#changepw .left-button').click(function() {
        resetForm('#changepw');
        swap('#change-password', '#your-account');
    });
    
    var success = function(data) {
        resetForm('#changepw');
        swap('#change-password', '#success');
    };
    
    popupForm('#changepw', null, success);
}

function initChangeEmailForm() {
    $('#changeemail .left-button').click(function() {
        resetForm('#changeemail');
        swap('#change-email', '#your-account');
    });
    
    var success = function(data) {
        // Put the new email value in the 'Your acount' popup
        var email = $('#changeemail-new_email input').val();
        $('#your-email span').text(email);
        
        resetForm('#changeemail');
        swap('#change-email', '#success');
    };
    
    popupForm('#changeemail', null, success);
}

function initDeleteAccountForm() {
    $('#delaccount .left-button').click(function() {
        resetForm('#delaccount');
        swap('#delete-account', '#your-account');
    });
    
    popupForm('#delaccount', null, function($form, data) {
        setTimeout(function() {
            // Redirect to next url if account deleted
            window.location.replace(data.next);
        }, 200);
    });
}

$(document).ready(function() {
    initPlaceholders();
    initChangePasswordForm();
    initChangeEmailForm();
    initDeleteAccountForm();
});