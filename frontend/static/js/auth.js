/*  Scripts for registration and authentication
*   for navbar.
*/


const SERVER_ERROR_MESSAGE = gettext('Something went wrong, try later.');
const EMAIL_INVALID_MESSAGE = gettext('Enter a valid email.');
const EMAIL_TAKEN_MESSAGE = gettext('This email is already taken.');


/**
 *  Get a Cookie value by a key. 
 *  From Django docs: https://docs.djangoproject.com/en/4.1/howto/csrf/
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}


/**
 *  Validate email address.
 * 
 *  @param {string} email: an email for validation.
 *  @returns {bool}: is valid or not.
 */
const validateEmail = (email) => {
    return email.match(
      /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
    );
};


/**
 *  An ajax request on sending the sing up email to a user.
 * 
 *  @param {string} email: user's email, where to send the sing up link.
 */
function sendSignupEmail(email) {
    const singup_email_url = document.getElementById('signup_email_url').innerHTML;
    const emailInputField = document.getElementById('user_email');
    const feedbackMessageElement = document.getElementById('user_email_feedback');
    document.getElementById('signup-sent-to').innerText = email;
    $.ajax({
        type: "POST",
        data: JSON.stringify({'email': email}),
        url: singup_email_url,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: function(data) {
            switch(data.msg) {
                case 'invalid':
                    emailInputField.classList.add('is-invalid');
                    feedbackMessageElement.innerHTML = EMAIL_INVALID_MESSAGE;
                    break;
                case 'sent':
                    $('#signup').modal('hide');
                    $('#signup-end').modal('show');
                    break;
                default:
                    emailInputField.classList.add('is-invalid');
                    feedbackMessageElement.innerHTML = SERVER_ERROR_MESSAGE;
            }
        },
        error: function (response) {
            console.log('`sendSignupEmail` faild.');
            emailInputField.classList.add('is-invalid');
            feedbackMessageElement.innerHTML = SERVER_ERROR_MESSAGE;
        },
        timeout: 3500
    });
}


/**
 *  An ajax request for checking email availabitily.
 * 
 *  @param {string} email: user's email for the form. 
 */
function isEmailAvailable(email) {
    const validate_url = document.getElementById('validate_email_url').innerHTML;
    const emailInputField = document.getElementById('user_email');
    const feedbackMessageElement = document.getElementById('user_email_feedback');
    $.ajax({
        type: 'GET',
        data: {'email': email},
        url: validate_url,
        headers: {"X-Requested-With": "XMLHttpRequest"},
        success: function(response) {
            if (response.is_taken == true) {
                // taken
                feedbackMessageElement.innerHTML = EMAIL_TAKEN_MESSAGE;
                emailInputField.classList.add('is-invalid');
            } else {
                // free
                feedbackMessageElement.innerHTML = ''
                emailInputField.classList.remove('is-invalid');
                sendSignupEmail(email);
            }
        },
        error: function (response) {
            feedbackMessageElement.innerHTML = SERVER_ERROR_MESSAGE;
            emailInputField.classList.add('is-invalid');
        },
        timeout: 2400
    });
}


/**
 *  On click validate email, then either call next function or show error messages.
 */
document.getElementById('submit_email').onclick = function() {
    const emailInputField = document.getElementById('user_email');
    const email = emailInputField.value;
    const feedbackMessageElement = document.getElementById('user_email_feedback');
    
    if (validateEmail(email)) {
        // valid
        feedbackMessageElement.innerHTML = '';
        emailInputField.classList.remove('is-invalid');
        // check email availability
        isEmailAvailable(email)
    } else {
        // invalid
        feedbackMessageElement.innerHTML = EMAIL_INVALID_MESSAGE;
        emailInputField.classList.add('is-invalid');
    }
}
