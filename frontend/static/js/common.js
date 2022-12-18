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
const styleLink = document.getElementById('color-theme');
function swapTheme(event) {
    const btn = event.target; 
    if (styleLink.href == lightThemeUrl.href) {
        styleLink.href = darkThemeUrl.href;
        btn.lastElementChild.innerText = gettext('Light theme');
        btn.firstElementChild.setAttribute('class', 'bi bi-brightness-high px-2');
        localStorage.setItem('theme', darkThemeUrl.href);
    } else {
        styleLink.href = lightThemeUrl.href;
        btn.lastElementChild.innerText = gettext('Dark theme');
        btn.firstElementChild.setAttribute('class', 'bi bi-brightness-high-fill px-2');
        localStorage.setItem('theme', lightThemeUrl.href);
    }
}
document.getElementById('theme-btn').onclick = swapTheme;
document.getElementById('theme-btn-2').onclick = swapTheme;
const theme = localStorage.getItem('theme');
if (theme == darkThemeUrl.href) {
    const btn1 = document.getElementById('theme-btn');
    const btn2 = document.getElementById('theme-btn-2');
    styleLink.href = darkThemeUrl.href;
    btn1.lastElementChild.innerText = gettext('Light theme');
    btn1.firstElementChild.setAttribute('class', 'bi bi-brightness-high px-2');
    btn2.lastElementChild.innerText = gettext('Light theme');
    btn2.firstElementChild.setAttribute('class', 'bi bi-brightness-high px-2');
}

