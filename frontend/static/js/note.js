// Bootstrap tooltip
const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

// Initialize context
const user_id = JSON.parse(document.getElementById('user_id').textContent);
const login_url = document.getElementById('login_url').innerHTML;
const post_url = document.getElementById('post_url').innerHTML

const like_html = '<i class="bi bi-heart"></i>';
const like_fill_html = '<i class="bi bi-heart-fill"></i>';

  // Set CSRF token to "X-CSRFToken" header
var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){
$('a.like').click(function(e){
    e.preventDefault();
    if (user_id == null) {  // if user is not logged in
    window.location.href = login_url;
    }
    $.post(post_url,
    {
    id: $(this).data('id'),
    action: $(this).data('action')
    },
    function(data){
    if (data['status'] == 'ok') {
        var previous_action = $('a.like').data('action');

        // toggle data-action
        $('a.like').data('action', previous_action == 'like' ? 'unlike' : 'like');

        // toggle like icon (link text)
        // toggle link text
        $('span.like').html(previous_action == 'like' ? like_fill_html : like_html);

        // update total likes
        var previous_likes = parseInt($('span.total_likes').text());
        $('span.total_likes').text(
        previous_action == 'like' ? previous_likes + 1 : previous_likes - 1
        );
    }
    });
});
});