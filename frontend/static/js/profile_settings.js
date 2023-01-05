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
};