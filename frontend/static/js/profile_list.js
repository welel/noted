function follow(event) {
    const followBtn = event.target;
    $.ajax({
        type: 'POST',
        url: document.getElementById('follow-url').href,
        data: {
            id: followBtn.getAttribute('user-id'),
            action: followBtn.getAttribute('action'),
        },
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        success: (res) => {
            let previous_action = followBtn.getAttribute('action');

            // toggle data-action
            followBtn.setAttribute('action',
                previous_action == 'follow' ? 'unfollow': 'follow');
            // toggle link text
            followBtn.innerText = previous_action == 'follow' ? gettext('Unsubscribe') : gettext('Follow');
        },
        error: (res) => {
            console.log('Bad Request: unable to follow.');
        },
        timeout: 3000
    });
}

buttons = document.getElementsByClassName('follow-btn')
for (let i = 0; i < buttons.length; i++ ) {
    buttons[i].onclick = follow;
}
