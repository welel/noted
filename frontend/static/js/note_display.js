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