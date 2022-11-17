    // Initilize context
    const post_url = document.getElementById('post_url').innerHTML;

    // Show notes without scrolling
    const animItems = document.querySelectorAll('._anim-items');
    for (let index = 0; index < animItems.length; index++) {
        const animItem = animItems[index];
        animItem.classList.add('_active');
     }

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

$(document).ready(function () {
     // Ajax request -follow/unfollow a user-
     $('a.follow').click(function(e) {
        e.preventDefault();
        $.post(post_url, 
            {
                id: $(this).data('id'),
                action: $(this).data('action')
            },
            function(data) {
                if (data['status'] == 'ok') {
                    let previous_action = $('a.follow').data('action');

                    // toggle data-action
                    $('a.follow').data('action',
                        previous_action == 'follow' ? 'unfollow': 'follow');
                    // toggle link text
                    $('a.follow').text(
                        previous_action == 'follow' ? 'Unsubscribe' : 'Follow'
                    );

                    // update total followers
                    let previous_followers = parseInt(
                        $('b.followers-count').text()
                    );
                    $('b.followers-count').text(
                        previous_action == 'follow' ? previous_followers + 1 : previous_followers - 1
                    );
                }
            }
        );
    });
});