from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from actions.models import Action
from user.models import Contact


@login_required(login_url=reverse_lazy('account_login'))
def feed(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = [contact.follower.id
                for contact in Contact.objects.filter(follower=request.user)]
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    actions = actions.select_related('user', 'user__profile')\
            .prefetch_related('target')[:10]
    return render(request, 'user/feed.html', {'actions': actions})


@login_required(login_url=reverse_lazy('account_login'))
def note_feed(request):
    actions = Action.objects.exclude(user=request.user)\
        .filter(verb=Action.NEW_NOTE)
    following_ids = [contact.follower.id
                for contact in Contact.objects.filter(follower=request.user)]
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
    # TODO: exclude private notes
    actions = actions.prefetch_related('target')
    notes = [actions.target for actions in actions]
    return render(request, 'notes/feed_list.html', {'actions': actions,
                                                   'notes': notes})
