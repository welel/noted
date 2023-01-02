// An ajax request for checking username availabitily.
const usernameInputField = document.getElementById('id_username');
const feedbackMessageElement = document.getElementById('invalid-username-message');

usernameInputField.onkeyup = (event) => {
    $.ajax({
        type: 'GET',
        data: {'username': usernameInputField.value},
        url: usernameValidationUrl,
        headers: {"X-Requested-With": "XMLHttpRequest"},
        success: function(response) {
            if (response.is_taken == true) {
                // taken
                feedbackMessageElement.innerHTML = gettext('Username is already taken.');
                usernameInputField.classList.remove('is-valid');
                usernameInputField.classList.add('is-invalid');
            } else if (response.is_taken == false) {
                // free
                usernameInputField.classList.remove('is-invalid');
                usernameInputField.classList.add('is-valid');
            } else if (response.is_taken == 'error') {
                feedbackMessageElement.innerHTML = gettext("Sorry, we can't change username now. Try later.");
                usernameInputField.classList.remove('is-valid');
                usernameInputField.classList.add('is-invalid');
            } else if (response.invalid) {
                feedbackMessageElement.innerHTML = response.invalid;
                usernameInputField.classList.remove('is-valid');
                usernameInputField.classList.add('is-invalid');
            }
        },
        error: function (response) {
            console.log(response.invalid, response.is_taken)
            
        },
        timeout: 2400
    });
}


const emailInputElement = document.getElementById('user-email');
const feedbackEmailElement = document.getElementById('user-email-feedback');
emailInputElement.onkeyup = (event) => {
    if (validateEmail(emailInputElement.value)) {
        setValid(emailInputElement, feedbackEmailElement);
        // check email availability
    } else {
        setInvalid(emailInputElement, feedbackEmailElement, EMAIL_INVALID_MESSAGE);
        
    }
};


/**
 *  An ajax request on sending the chaning email message to a user.
 */
function sendChangeEmailToken() {
    $.ajax({
        type: "POST",
        data: JSON.stringify({'email': emailInputElement.value}),
        url: changeEmailRequestUrl,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: (data) => {
            switch(data.msg) {
                case 'invalid':
                    setInvalid(emailInputElement, feedbackEmailElement, EMAIL_INVALID_MESSAGE);
                    break;
                case 'sent':
                    $('#change-email-modal').modal('hide');
                    $('#change-email-end').modal('show');
                    break;
                default:
                    setInvalid(emailInputElement, feedbackEmailElement, SERVER_ERROR_MESSAGE);
            }
        },
        error: (response) => {
            console.log('`sendChangeEmailToken` faild.', response);
            setInvalid(emailInputElement, feedbackEmailElement, SERVER_ERROR_MESSAGE);
        },
        timeout: 3500
    });
}


/**
 *  An ajax request for checking email availabitily and send token.
 */
function isEmailTaken() {
    $.ajax({
        type: 'GET',
        data: {'email': emailInputElement.value},
        url: emailValidationUrl,
        headers: {"X-Requested-With": "XMLHttpRequest"},
        success: function(response) {
            if (response.is_taken == true) {
                setInvalid(emailInputElement, feedbackEmailElement, EMAIL_TAKEN_MESSAGE);
            } else {
                setValid(emailInputElement, feedbackEmailElement);
                sendChangeEmailToken();
            }
        },
        error: function (response) {
            setInvalid(emailInputElement, feedbackEmailElement, SERVER_ERROR_MESSAGE);
        },
        timeout: 2400
    });
}


document.getElementById('submit-email').onclick = (event) => {
    if (validateEmail(emailInputElement.value)) {
        isEmailTaken();
    }
};
