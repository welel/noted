from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required

from user.forms import UserForm, ProfileForm
from user.models import User, Contact
from notes.models import Note


@login_required(login_url=reverse_lazy('account_login'))
def edit_user(request):
    """Handle :model:`user.User` and :model:`user.Profile` editing forms.
    
    **Context**
        user_form: a form for :model:`user.User`.
        profile_form: a form for :model:`user.Profile`.

    **Template**
        :template:`frontend/templates/user/account/edit.html`
    """
    if request.method == 'POST':
        user_form = UserForm(instance=request.user, data=request.POST)
        profile_form = ProfileForm(request.POST, request.FILES,
            instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'user/account/edit.html', {'user_form': user_form,
        'profile_form': profile_form})


def profile(request, username):
    """Display user profile page.
    
    **Context**
        user: a user instance :model:`user.User`.
        profile: a user profile instance :model:`user.Profile`.
        notes: user's notes.
        num_likes: like number for all user's notes.
        followers: followers of a user.
        following: user's subscriptions.

    **Template**
        :template:`frontend/templates/user/account/profile.html`
    """
    user = get_object_or_404(User, username=username)
    profile = user.profile
    notes = Note.objects.public().filter(author=user)
    notes = notes.annotate(num_likes=Count('users_like'))
    total_user_likes = sum([note.num_likes for note in notes])
    followers = [contact.follower 
                    for contact in Contact.objects.filter(followed=user)]
    following = [contact.following 
                    for contact in Contact.objects.filter(followed=user)]
    return render(request, 'user/account/profile.html',
                    {'user': user, 'profile': profile,
                     'notes': notes, 'num_likes': total_user_likes,
                     'followers': followers, 'following': following}
    )


@login_required(login_url=reverse_lazy('account_login'))
def delete(request):
    """Delete a user."""
    if request.method == 'POST':
        request.user.delete()
    return redirect('account_signup')


@ajax_required
@require_POST
@login_required(login_url=reverse_lazy('account_login'))
def user_follow(request):
    """Handle ajax request - follow/unfollow a user.
    
    **Post params**
        id: id of a user is going to be followed.
        action: follow/unfollow.
    """
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(followed=user,
                                              follower=request.user)
            else:
                Contact.objects.filter(followed=user,
                    follower=request.user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
