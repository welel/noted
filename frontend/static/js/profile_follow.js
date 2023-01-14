const followBtn = document.getElementById('follow-btn');
followBtn.onclick = (event) => {
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

            // update total followers
            let previous_followers = parseInt(document.getElementById('followers-counter').innerText);
            document.getElementById('followers-counter').innerText = previous_action == 'follow' ? previous_followers + 1 : previous_followers - 1;
        },
        error: (res) => {
            console.log('Bad Request: unable to follow.');
        },
        timeout: 3000
    });
};
