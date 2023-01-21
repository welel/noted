function readNotice(slug) {
    $.ajax({
        type: 'GET',
        url: readNoticeUrl,
        headers: {"X-Requested-With": "XMLHttpRequest"},
        data: {'slug': slug},
        success: (res) => {
            if (res.read) {
                document.getElementById(`read-btn-${slug}`).hidden = true;
            }
        },
        error: (res) => {
            console.log('Server problem: can\'t read the notification.')
        },
        timeout: 2500
    })
}


function deleteNotice(slug) {
    $.ajax({
        type: 'GET',
        url: deleteNoticeUrl,
        headers: {"X-Requested-With": "XMLHttpRequest"},
        data: {'slug': slug},
        success: (res) => {
            if (res.deleted) {
                document.getElementById(`notice-${slug}`).hidden = true;
            }
        },
        error: (res) => {
            console.log('Server problem: can\'t delete the notification.')
        },
        timeout: 2500
    })
}