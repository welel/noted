const tagFollowBtn = document.getElementById('follow-tag');

tagFollowBtn.onclick = (event) => {
    $.ajax({
        type: 'GET',
        url: document.getElementById('follow-tag-url').innerText,
        headers: {"X-Requested-With": "XMLHttpRequest"},
        success: (res) => {
            if (res.result == 'added') {
                tagFollowBtn.innerText = gettext('Unfollow');
            } else {
                tagFollowBtn.innerText = gettext('Follow');
            }
        },
        error: (res) => {
            console.log('Unable to follow/unfollow.')
        },
        timeout: 2000
    });
}