from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy

from user.forms import UserForm, ProfileForm
from user.models import User
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
    """Display user fields, profile and notes of a user."""
    user = get_object_or_404(User, username=username)
    profile = user.profile
    notes = Note.objects.public().filter(author=user)
    return render(request, 'user/account/profile.html', {'user': user,
                                                         'profile': profile,
                                                         'notes': notes})


@login_required(login_url=reverse_lazy('account_login'))
def delete(request):
    """Delete a user."""
    if request.method == 'POST':
        request.user.delete()
    return redirect('account_signup')
