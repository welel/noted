/*  Scripts for registration and authentication
*   for navbar.
*/


const SERVER_ERROR_MESSAGE = gettext('Something went wrong, try later.');
const EMAIL_INVALID_MESSAGE = gettext('Enter a valid email.');
const EMAIL_TAKEN_MESSAGE = gettext('This email is already taken.');
const EMPTY_PASSWORD_INVALID_MESSAGE = gettext('Enter password.');


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


function getStatus(taskID, successModalId) {
    $.ajax({
      url: taskStatusUrl,
      data: {"task_id": taskID},
      method: 'GET',
      headers: {"X-Requested-With": "XMLHttpRequest"},
      success: (res) => {
          const taskStatus = res.task_status;
          const taskResult = res.task_result;
      
          if (taskStatus === 'SUCCESS' && taskResult) {
            $(successModalId).modal('show');
            return false;
          }
          setTimeout(function() {
            getStatus(res.task_id, successModalId);
          }, 1000);
      },
      error: (res) => {
        $('#server-error-modal').modal('show');
        console.log("A task faield: " + res)
      }
    })
  }


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
                case 'started':
                    $('#signup').modal('hide');
                    getStatus(data.task_id, '#signup-end');
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
                feedbackMessageElement.innerHTML = '';
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


/**
 *  An sign-in ajax request.
 * 
 *  @param {string} email: user's email from the form. 
 *  @param {string} password: user's password from the form.
 */
 function signin(email, password) {
    const signinUrl = document.getElementById('signin_url').innerHTML;
    const emailInputField = document.getElementById('signin_email');
    const emailFeedbackMessageElement = document.getElementById('signin_email_feedback');
    const passwordInputField = document.getElementById('signin_password');
    const passwordFeedbackMessageElement = document.getElementById('signin_password_feedback');
    const signinFeedbackMessageElement = document.getElementById('signin_feedback');
    $.ajax({
        type: 'POST',
        data: JSON.stringify({'email': email, 'password': password}),
        url: signinUrl,
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: function(response) {
            console.log('success', response)
            switch(response.code) {
                case 'noemail':
                    emailFeedbackMessageElement.innerHTML = response.error_message;
                    emailInputField.classList.add('is-invalid');
                    break;
                case 'badpass':
                    passwordFeedbackMessageElement.innerHTML = response.error_message;
                    passwordInputField.classList.add('is-invalid');
                    break;
                case 'success':
                    window.location.href = response.redirect_url;
            }
        },
        error: function (response) {
            console.log(response)
            signinFeedbackMessageElement.innerHTML = SERVER_ERROR_MESSAGE;
        },
        timeout: 3500
    });
}


/**
 *  On click validate signin form, then either call next function or show error messages.
 */
 document.getElementById('signin_submit').onclick = function() {
    const emailInputField = document.getElementById('signin_email');
    const email = emailInputField.value;
    const emailFeedbackMessageElement = document.getElementById('signin_email_feedback');
    const passwordInputField = document.getElementById('signin_password');
    const password = passwordInputField.value;
    const passwordFeedbackMessageElement = document.getElementById('signin_password_feedback');
    
    if (validateEmail(email)) {
        // valid
        emailFeedbackMessageElement.innerHTML = '';
        emailInputField.classList.remove('is-invalid');
    } else {
        // invalid
        emailFeedbackMessageElement.innerHTML = EMAIL_INVALID_MESSAGE;
        emailInputField.classList.add('is-invalid');
        return
    }

    if (password != '') {
        // valid
        passwordFeedbackMessageElement.innerHTML = '';
        passwordInputField.classList.remove('is-invalid');
    } else {
        // invalid
        passwordFeedbackMessageElement.innerHTML = EMPTY_PASSWORD_INVALID_MESSAGE;
        passwordInputField.classList.add('is-invalid');
        return
    }
    signin(email, password)
}


// Submit sign up form on Enter
document.getElementById('user_email').addEventListener('keypress', (event) => {
    if (event.key == "Enter") {
        document.getElementById('submit_email').click();
    }
});


// Submit sign in form on Enter
document.getElementById('signin_password').addEventListener('keypress', (event) => {
    if (event.key == "Enter") {
        document.getElementById('signin_submit').click();
    }
});