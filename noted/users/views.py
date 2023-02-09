from abc import ABC, abstractclassmethod
import json
import logging
from typing import Callable

from allauth.account.models import EmailAddress

from django.contrib import messages as msg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as _validate_email
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import generic, View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

from common import logging as log
from common.logging import LoggerDecorator as logg
from common.decorators import ajax_required
from content.models import Note

from .auth import (
    send_changeemail_email,
    send_signup_email,
    unsign_email,
    MESSAGES,
)
from .forms import DeleteAccount, SignupForm, UpdateUserForm, UserProfileForm
from .forms import validate_username
from .models import AuthToken, Following, User

logger = logging.getLogger(__name__)


@method_decorator(ajax_required, name="dispatch")
class TokenizedEmailView(ABC, View):
    """An abstract view class for sending tokenized emails to a user."""

    @abstractclassmethod
    def get_send_email_function(self) -> Callable:
        """Returns a funtion for sending emails.

        The functions should take one positional argument - email (str),
        which is an addressee.
        """
        pass

    def post(self, request):
        email = json.load(request).get("email")
        try:
            _validate_email(email)
        except ValidationError:
            return JsonResponse({"msg": "invalid"}, status=200)
        if self.get_send_email_function()(email):
            return JsonResponse({"msg": "sent"}, status=200)
        return JsonResponse({"msg": "error"}, status=200)


class SignupEmailView(TokenizedEmailView):
    """Send sing up email to a client with the link to the sign up form."""

    def get_send_email_function(self) -> Callable:
        return send_signup_email


class ChangeemailEmailView(TokenizedEmailView):
    """Send change email message to a client with the link to the change view."""

    def get_send_email_function(self) -> Callable:
        return send_changeemail_email


@method_decorator(ajax_required, name="dispatch")
class EmailExistanceCheckView(View):
    @logg("view_exception")
    def get(self, request):
        """Check if a user with a given email already exists in the database."""
        email = request.GET.get("email")
        response = {
            "is_taken": EmailAddress.objects.filter(email=email).exists()
            or User.objects.filter(email=email).exists()
        }
        return JsonResponse(response, status=200)


@method_decorator(ajax_required, name="dispatch")
class UsernameExistanceCheckView(View):
    def get(self, request):
        """Check if a user with a given username already exists in the database."""
        username = request.GET.get("username")
        username = "@" + username if username else None
        try:
            validate_username(username)
        except ValidationError as error:
            return JsonResponse({"invalid": str(error.message)}, status=200)
        response = {
            "is_taken": User.objects.filter(username=username).exists()
            and not username == request.user.username
        }
        return JsonResponse(response, status=200)


class ChangeEmailView(LoginRequiredMixin, View):
    def get(self, request, token: str):
        """Handles change email request (works by the link from an email message).

        Args:
            token: A unique token of a client for chaning email.
        """
        try:
            token = AuthToken.objects.get(
                token=token, type=AuthToken.CHANGE_EMAIL
            )
        except AuthToken.DoesNotExist:
            msg.add_message(request, msg.WARNING, MESSAGES["ce_token_miss"])
            return redirect(reverse("content:home"))

        email, error = unsign_email(token)
        if error:
            logger.warning(
                log.VIEW_LOG_TEMPLATE.format(
                    name=ChangeEmailView.__name__,
                    user=request.user,
                    method=request.method,
                    path=request.path,
                )
                + f"User have problems with changing email signature: token id {token.pk}"
            )
            return render(
                request,
                "error.html",
                {"message": error, "title": error},
            )

        # You can't change your email if you signed up via a third paty service.
        if EmailAddress.objects.filter(email=email).exists():
            msg.add_message(request, msg.WARNING, MESSAGES["signed_social"])
            return redirect(reverse("content:home"))

        request.user.email = email
        request.user.save()
        msg.add_message(request, msg.INFO, MESSAGES["email_changed"])
        token.delete()
        return redirect(reverse("content:home"))


def signup(request, token):
    """Sign up process.

    Args:
        token (str): a unique token of a client for registration.

    Validates token.
    GET: provides the registration form.
    POST: validates data, creates new user, deletes the token.
    """
    template_name = "users/signup.html"
    context = {"token": token}

    try:
        token = AuthToken.objects.get(token=token, type=AuthToken.SIGNUP)
    except AuthToken.DoesNotExist:
        msg.add_message(request, msg.WARNING, MESSAGES["su_token_miss"])
        return redirect(reverse("content:home"))

    email, error = unsign_email(token)
    if error:
        logger.warning(
            log.VIEW_LOG_TEMPLATE.format(
                name=signup.__name__,
                user=request.user,
                method=request.method,
                path=request.path,
            )
            + f"User have problems with sign up signature: token id {token.pk}"
        )
        return render(request, template_name, {"error": error})

    if request.method == "GET":
        form = SignupForm()
        context["form"] = form
        return render(request, template_name, context)

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = email
            user.is_active = True
            user.save()
            token.delete()
            if user:
                login(
                    request,
                    user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
            logger.info("New user sign up:" + str(user))
            return redirect(reverse("content:home"))
        else:
            context["form"] = form
            return render(request, template_name, context)


@ajax_required
def signin(request):
    """Sign in a user via ajax request."""
    if request.method == "POST":
        data = json.load(request)
        email = data.get("email")
        password = data.get("password")
        if not User.objects.filter(email=email).exists():
            return JsonResponse(
                {"code": "noemail", "error_message": MESSAGES["noemail"]}
            )
        user = authenticate(email=email, password=password)
        if not user:
            return JsonResponse(
                {"code": "badpass", "error_message": MESSAGES["wrong_pass"]}
            )
        login(
            request, user, backend="django.contrib.auth.backends.ModelBackend"
        )
        # TODO: redirect on referer
        return JsonResponse(
            {"code": "success", "redirect_url": reverse("content:home")}
        )
    return HttpResponseBadRequest()


def signout(request):
    logout(request)
    return redirect(reverse("content:home"))


def delete_account(request):
    if request.method == "GET":
        form = DeleteAccount()
        return render(request, "users/delete_account.html", {"form": form})
    elif request.method == "POST":
        form = DeleteAccount(request.POST)
        if form.is_valid():
            method = form.cleaned_data.get("method_select")
            if method == "save":
                for note in Note.objects.filter(author=request.user):
                    note.anonymous = True
                    note.save()
            elif method == "delete":
                for note in Note.objects.filter(author=request.user):
                    note.delete()
            request.user.delete()
            return redirect("content:welcome")
        return render(request, "users/delete_account.html", {"form": form})
    return HttpResponseBadRequest()


class UpdateUserProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = "users/profile_settings.html"

    def get(self, request, *args, **kwargs):
        user_form = UpdateUserForm(instance=request.user)
        # Cut '@' sign.
        user_form.initial["username"] = user_form.initial["username"][1:]
        profile_form = UserProfileForm(instance=request.user.profile)
        profile_form.initial.update(request.user.profile.get_socials())
        self.extra_context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "user": get_object_or_404(User, pk=request.user.pk),
            "social_account": EmailAddress.objects.filter(
                email=request.user.email
            ).exists(),
        }
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        else:
            return render(
                request,
                self.template_name,
                {
                    "user_form": user_form,
                    "profile_form": profile_form,
                    "user": get_object_or_404(User, pk=request.user.pk),
                    "social_account": EmailAddress.objects.filter(
                        email=request.user.email
                    ).exists(),
                },
            )
        return redirect("users:settings")


@ajax_required
@require_POST
@login_required
def user_follow(request):
    """Handle ajax request - follow/unfollow a user.

    **Post params**
        id: id of a user is going to be followed.
        action: follow/unfollow.
    """
    try:
        user_id = int(request.POST.get("id"))
    except TypeError:
        user_id = 0
    action = request.POST.get("action")

    if user_id and action and request.user.id != user_id:
        user = get_object_or_404(User, id=user_id)
        following, _ = Following.objects.get_or_create(
            followed=user, follower=request.user
        )
        if action == "unfollow":
            following.delete()
        return JsonResponse({"status": "ok"})

    return JsonResponse({"status": "error"})
