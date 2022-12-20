// Ajax request to like the note (toggle `like` note instance field value).
function bookmarkNote(note_pk) {
    const bookmarkButton = document.getElementById(`bookmark-btn-${note_pk}`);
    const bookmarkIcon = bookmarkButton.firstElementChild.firstElementChild;
    const url = bookmarkButton.getAttribute('url');
    $.ajax({
        type: 'GET',
        url: url,
        headers: {"X-Requested-With": "XMLHttpRequest"},
        success: (res) => {
            if (res.bookmarked) {
                bookmarkIcon.setAttribute('class', 'bi bi-bookmark-plus-fill');
            }
            if (!res.bookmarked) {
                bookmarkIcon.setAttribute('class', 'bi bi-bookmark-plus');
            }
        },
        error: (res) => {
            console.log('Bad Request: unable to bookmark.');
        },
        timeout: 3000
    });
}

function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
            tmp = item.split("=");
            if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}
