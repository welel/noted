from abc import ABC, abstractclassmethod
import json
import logging
from typing import Callable, Type

from django.conf import settings
from django.contrib import messages as msg
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as _validate_email
from django.db.transaction import atomic
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _
from django.views import generic, View
from django.utils.decorators import method_decorator

from allauth.account.models import EmailAddress

from common.logging import LoggerDecorator as logit
from common.decorators import ajax_required
from content.models import Note

from .auth import (
    send_changeemail_email,
    send_signup_email,
    unsign_email,
    MESSAGES,
    StringToken,
    TokenData,
    get_token,
)
from .forms import (
    DeleteUserForm,
    SignupForm,
    UpdateUserForm,
    UserProfileForm,
    validate_username,
)
from .models import AuthToken, Following, User


logger = logging.getLogger(__name__)


@method_decorator(logit(__name__), name="dispatch")
@method_decorator(ajax_required(type="method"), name="dispatch")
class TokenizedEmailView(ABC, View):
    """An abstract view class for sending tokenized emails to a user."""

    @abstractclassmethod
    def get_send_email_function(self) -> Callable:
        """Returns a funtion for sending emails.

        The functions should take one positional argument - email (str),
        which is an addressee.
        """
        ...

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


@method_decorator(logit(__name__), name="dispatch")
@method_decorator(ajax_required(), name="dispatch")
class EmailExistanceCheckView(View):
    def get(self, request):
        """Check if a user with a given email already exists in the database."""
        email = request.GET.get("email")
        response = {
            "is_taken": EmailAddress.objects.filter(email=email).exists()
            or User.objects.filter(email=email).exists()
        }
        return JsonResponse(response, status=200)


@method_decorator(logit(__name__), name="dispatch")
@method_decorator(ajax_required(), name="dispatch")
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


class TokenMixin:
    token_type: str
    token_miss_error: str

    def get_token_data(self, token: str) -> TokenData:
        token = get_token(StringToken(token=token, type=self.token_type))
        if not token:
            return TokenData(error=self.token_miss_error)

        email, error = unsign_email(token)
        if error:
            return TokenData(error=error)

        return TokenData(token=token, email=email)


@method_decorator(logit(__name__), name="dispatch")
class ChangeEmailView(LoginRequiredMixin, TokenMixin, View):
    token_type = AuthToken.CHANGE_EMAIL
    token_miss_error = MESSAGES["ce_token_miss"]

    def get(self, request, token: str):
        """Handles change email request (works by the link from an email message).

        Args:
            token: A unique token of a client for chaning email.
        """
        token, email, error = self.get_token_data(token)
        if error:
            context = {"title": _("Token Error"), "message": error}
            return render(request, "error.html", context)

        # You can't change your email if you signed up via a third paty service.
        if EmailAddress.objects.filter(email=email).exists():
            msg.add_message(request, msg.WARNING, MESSAGES["signed_social"])
            return redirect(reverse("users:settings"))
        with atomic():
            request.user.update(email=email)
            token.delete()
        msg.add_message(request, msg.INFO, MESSAGES["email_changed"])
        return redirect(reverse("content:home"))


@method_decorator(logit(__name__), name="dispatch")
class SignupView(TokenMixin, View):
    template_name = "users/signup.html"
    token_type = AuthToken.SIGNUP
    token_miss_error = MESSAGES["su_token_miss"]

    def get(self, request, token: str):
        """Validates a sign up token and provides the registration form.

        Args:
            token: A unique token of a client for registration.
        """
        context = {"token": token}
        __, __, error = self.get_token_data(token)
        if error:
            context = {"title": _("Token Error"), "message": error}
            return render(request, "error.html", context)

        form = SignupForm()
        context["form"] = form
        return render(request, self.template_name, context)

    def post(self, request, token: str):
        """Validates data, creates new user, deletes the token.

        Args:
            token: A unique token of a client for registration.
        """
        context = {"token": token}
        token, email, error = self.get_token_data(token)
        if error:
            context = {"title": _("Token Error"), "message": error}
            return render(request, "error.html", context)

        form = SignupForm(request.POST)
        if form.is_valid():
            with atomic():
                user = form.save(commit=False)
                user.update(email=email, is_active=True)
                token.delete()
            login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
            return redirect(reverse("content:home"))
        else:
            context["form"] = form
            return render(request, self.template_name, context)


@method_decorator(logit(__name__), name="dispatch")
class SigninView(View):
    @ajax_required(type="method")
    def post(self, request):
        """Sign in a user via ajax request."""
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
        login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
        redirect_url = request.headers.get("referer", reverse("content:home"))
        return JsonResponse({"code": "success", "redirect_url": redirect_url})


@method_decorator(logit(__name__), name="dispatch")
class DeleteUserView(LoginRequiredMixin, View):
    template_name = "users/delete_account.html"
    success_redirect_name = "content:welcome"

    def get(self, request):
        return render(request, self.template_name, {"form": DeleteUserForm()})

    def post(self, request):
        form = DeleteUserForm(request.POST)
        if form.is_valid():
            user_notes = Note.objects.filter(author=request.user)
            method = form.cleaned_data.get("delete_method")
            with atomic():
                if method == DeleteUserForm.KEEP_NOTES:
                    user_notes.update(anonymous=True)
                else:
                    user_notes.delete()
                request.user.delete()
            return redirect(self.success_redirect_name)
        return render(request, self.template_name, {"form": form})


@method_decorator(logit(__name__), name="dispatch")
class UpdateUserProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = "users/profile_settings.html"

    def get(self, request, *args, **kwargs):
        user_form = UpdateUserForm(instance=request.user)
        # Cut '@' sign.
        user_form.initial["username"] = user_form.initial["username"][1:]
        profile_form = UserProfileForm(instance=request.user.profile)
        profile_form.initial.update(request.user.profile.get_socials())
        self.set_extra_context(user_form, profile_form, request)
        return super().get(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            with atomic():
                user_form.save()
                profile_form.save()
        else:
            self.set_extra_context(user_form, profile_form, request)
            return render(request, self.template_name, self.get_context_data())
        return redirect("users:settings")

    def set_extra_context(
        self,
        user_form: UpdateUserForm,
        profile_form: UserProfileForm,
        request: Type[HttpRequest],
    ) -> None:
        self.extra_context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "user": get_object_or_404(User, pk=request.user.pk),
            "social_account": EmailAddress.objects.filter(
                email=request.user.email
            ).exists(),
        }


@method_decorator(logit(__name__), name="dispatch")
@method_decorator(ajax_required(type="method"), name="dispatch")
class FollowUserView(LoginRequiredMixin, View):
    def post(self, request):
        """Handle ajax request - follow/unfollow a user.

        **POST params**
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
