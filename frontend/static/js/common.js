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


// Color theme toggle
const lightThemeUrl = document.getElementById('css-light-theme-url'); 
const darkThemeUrl = document.getElementById('css-dark-theme-url');
const themeBtn = document.getElementById('theme-btn')
const styleLink = document.getElementById('color-theme');
themeBtn.onclick = (event) => {
    if (styleLink.href == lightThemeUrl.href) {
        styleLink.href = darkThemeUrl.href;
        themeBtn.lastElementChild.innerText = gettext('Light theme');
        themeBtn.firstElementChild.setAttribute('class', 'bi bi-brightness-high px-2');
        localStorage.setItem('theme', darkThemeUrl.href);
    } else {
        styleLink.href = lightThemeUrl.href;
        themeBtn.lastElementChild.innerText = gettext('Dark theme');
        themeBtn.firstElementChild.setAttribute('class', 'bi bi-brightness-high-fill px-2');
        localStorage.setItem('theme', lightThemeUrl.href);
    }
}
const theme = localStorage.getItem('theme');
if (theme == darkThemeUrl.href) {
    styleLink.href = darkThemeUrl.href;
    themeBtn.lastElementChild.innerText = gettext('Light theme');
    themeBtn.firstElementChild.setAttribute('class', 'bi bi-brightness-high px-2');
}

