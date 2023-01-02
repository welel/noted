// Ajax request to add/remove the note to/from bookmarks.
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


function setValid(element, feedback) {
    feedback.innerHTML = '';
    element.classList.remove('is-invalid');
    element.classList.add('is-valid');
}


function setInvalid(element, feedback, message) {
    feedback.innerHTML = message;
    element.classList.remove('is-valid');
    element.classList.add('is-invalid');
}