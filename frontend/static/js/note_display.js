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
    document.getElementById('copy-note-link').firstElementChild.setAttribute("class", "bi bi-check-lg link-h px-2 color-grey");
}
document.getElementById('copy-note-link').addEventListener('mouseout', (event) => {
    document.getElementById('copy-note-link').firstElementChild.setAttribute("class", "bi bi-link-45deg link-h px-2 color-grey");
});

// Copy current URL to clipboard
document.getElementById('copy-note-link2').onclick = (event) => {
    copyToClipboard(window.location.href);
}

// Ajax request to pin the note (toggle `pin` note instance field value).
const pinButton = document.getElementById('pin');
const pinButton2 = document.getElementById('pin-2');
// callback
function togglePin() {
    $.ajax({
        type: 'GET',
        url: document.getElementById('pin-note-url').innerText,
        headers: {"X-Requested-With": "XMLHttpRequest"},
        success: (res) => {
            if (res.pin) {
                pinButton.firstChild.setAttribute('class', 'bi bi-pin-angle-fill');
                pinButton2.firstChild.setAttribute('class', 'bi bi-pin-angle-fill');
                pinButton.lastChild.innerText = gettext('Unpin');
                pinButton2.lastChild.innerText = gettext('Unpin');
            }
            if (!res.pin) {
                pinButton.firstChild.setAttribute('class', 'bi bi-pin-angle');
                pinButton2.firstChild.setAttribute('class', 'bi bi-pin-angle');
                pinButton.lastChild.innerText = gettext('Pin');
                pinButton2.lastChild.innerText = gettext('Pin');
            }
        },
        error: (res) => {
            console.log('Bad Request: unable to pin.');
        },
        timeout: 3000
    });
}
if (pinButton) {
    pinButton.onclick = togglePin;
    pinButton2.onclick = togglePin;
}


// Ajax request to like the note (toggle `like` note instance field value).
const likeButton = document.getElementById('like-btn');
const likeIcon = likeButton.firstElementChild.firstElementChild;
const likeCount = likeButton.firstElementChild.lastElementChild;
likeButton.onclick = (event) => {
    if (likeButton.getAttribute('is-user-auth') == 'True') {
        $.ajax({
            type: 'GET',
            url: document.getElementById('like-note-url').innerText,
            headers: {"X-Requested-With": "XMLHttpRequest"},
            success: (res) => {
                if (res.liked) {
                    likeIcon.setAttribute('class', 'bi bi-heart-fill');
                    likeCount.innerText = Number(likeCount.innerText) + 1;
                }
                if (!res.liked) {
                    likeIcon.setAttribute('class', 'bi bi-heart');
                    likeCount.innerText = Number(likeCount.innerText) - 1;
                }
            },
            error: (res) => {
                console.log('Bad Request: unable to like.');
            },
            timeout: 3000
        });
    }
}



// Ajax request to like the note (toggle `like` note instance field value).
const bookmarkButton1 = document.getElementById('bookmark-btn-1');
const bookmarkButton2 = document.getElementById('bookmark-btn-2');
const bookmarkIcon1 = bookmarkButton1.firstElementChild;
const bookmarkIcon2 = bookmarkButton2.firstElementChild;
// callback
function toggleBookmark() {
    $.ajax({
        type: 'GET',
        url: document.getElementById('bookmark-note-url').innerText,
        headers: {"X-Requested-With": "XMLHttpRequest"},
        success: (res) => {
            if (res.bookmarked) {
                bookmarkIcon1.setAttribute('class', 'bi bi-bookmark-plus-fill link-h ps-2 color-grey');
                bookmarkIcon2.setAttribute('class', 'bi bi-bookmark-plus-fill link-h ps-3 color-grey');
            }
            if (!res.bookmarked) {
                bookmarkIcon1.setAttribute('class', 'bi bi-bookmark-plus link-h ps-2 color-grey');
                bookmarkIcon2.setAttribute('class', 'bi bi-bookmark-plus link-h ps-3 color-grey');
            }
        },
        error: (res) => {
            console.log('Bad Request: unable to bookmark.');
        },
        timeout: 3000
    });
}
bookmarkButton1.onclick = toggleBookmark;
bookmarkButton2.onclick = toggleBookmark;


// Add button to a code block to open the code block in fullscreen.
function addFullScreenBtnsToCodeBlock() {
    document.querySelectorAll('pre').forEach(function(pre, i) {
        pre.setAttribute('id', `code-block-${i}`);
        const btn = document.createElement('button');
        btn.setAttribute('id', `code-block-btn-${i}`);
        btn.addEventListener('click', function(){
            if (document.fullscreenElement) {
                document.exitFullscreen();
            } else {
                $(`#code-block-${i}`).get(0).requestFullscreen();
            }
        });
        btn.innerHTML = '<i class="bi bi-arrows-fullscreen"></i>';
        pre.insertBefore(btn, pre.firstElementChild);
        // Move button along on scroll code block
        pre.addEventListener("scroll", function(e) {
            btn.style.right = `-${pre.scrollLeft}px`; 
        });
    });
}

function completeDownloading(taskStatusUrl, taskId) {
    $.ajax({
        url: taskStatusUrl,
        data: {"task_id": taskId},
        method: 'GET',
        headers: {"X-Requested-With": "XMLHttpRequest"},
        xhrFields: {
            responseType: 'blob' // to avoid binary data being mangled on charset conversion
        },
        success: (blob, status, xhr) => {
            console.log(blob, status, xhr)
            if (xhr.status == 200) {
                var filename = "";
                var disposition = xhr.getResponseHeader('Content-Disposition');
                if (disposition && disposition.indexOf('attachment') !== -1) {
                    var filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    var matches = filenameRegex.exec(disposition);
                    if (matches != null && matches[1]) filename = matches[1].replace(/['"]/g, '');
                }
                
                if (typeof window.navigator.msSaveBlob !== 'undefined') {
                    // IE workaround for "HTML7007: One or more blob URLs were revoked by closing the blob for which they were created. These URLs will no longer resolve as the data backing the URL has been freed."
                    window.navigator.msSaveBlob(blob, filename);
                } else {
                    var URL = window.URL || window.webkitURL;
                    var downloadUrl = URL.createObjectURL(blob);
        
                    if (filename) {
                        // use HTML5 a[download] attribute to specify filename
                        var a = document.createElement("a");
                        // safari doesn't support this yet
                        if (typeof a.download === 'undefined') {
                            window.location.href = downloadUrl;
                        } else {
                            a.href = downloadUrl;
                            a.download = filename;
                            document.body.appendChild(a);
                            a.click();
                        }
                    } else {
                        window.location.href = downloadUrl;
                    }
        
                    setTimeout(function () { URL.revokeObjectURL(downloadUrl); }, 100); // cleanup
                }
                return;
            } else if (xhr.status == 202) {
                setTimeout(function() {
                    completeDownloading(taskStatusUrl, taskId);
                }, 1000);
            } else {
                return;
            }
        },
        error: (blob, status, xhr) => {
          console.log("Downloading of a task is faield: ", status)
        }
      })
}

function startNoteDownload(filetype) {
    let startNoteDownloadUrl;
    switch (filetype) {
        case 'html':
            startNoteDownloadUrl = startNoteDownloadHtmlUrl;
            break;
        case 'md':
            startNoteDownloadUrl = startNoteDownloadMdUrl;
            break;
        default:
            startNoteDownloadUrl = startNoteDownloadPdfUrl;
            break;
    }
    $.ajax({
        type: 'GET',
        url: startNoteDownloadUrl,
        headers: {"X-Requested-With": "XMLHttpRequest"},
        success: (res) => {
            completeDownloading(noteDownloadPoolingUrl, res.task_id);
        },
        error: (res) => {
            console.log('Bad Request: unable to download.');
        },
        timeout: 3000
    });
}

document.addEventListener('DOMContentLoaded', function(){
    addFullScreenBtnsToCodeBlock();
});