function copyToClipboard(text) {
    var clipboard = document.createElement('input');
    document.body.appendChild(clipboard);
    clipboard.value = text;
    clipboard.select();
    document.execCommand('copy');
    document.body.removeChild(clipboard);
}

// Copy current URL to clipboard
document.getElementById('copy-note-link').onclick = (event) => {
    copyToClipboard(window.location.href);
}

// Copy current URL to clipboard
document.getElementById('copy-note-link2').onclick = (event) => {
    copyToClipboard(window.location.href);
}

// Ajax request to pin the note (toggle `pin` note instance field value).
const pinButton = document.getElementById('pin');
pinButton.onclick = (event) => {
    $.ajax({
        type: 'GET',
        url: document.getElementById('pin-note-url').innerText,
        headers: {"X-Requested-With": "XMLHttpRequest"},
        success: (res) => {
            if (res.pin == true) {
                pinButton.firstChild.setAttribute('class', 'bi bi-pin-angle-fill');
                pinButton.lastChild.innerText = gettext('Unpin');
            }
            if (res.pin == false) {
                pinButton.firstChild.setAttribute('class', 'bi bi-pin-angle');
                pinButton.lastChild.innerText = gettext('Pin');
            }
        },
        error: (res) => {
            console.log('Bad Request: unable to pin.');
        },
        timeout: 2000
    });
}