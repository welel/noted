import logging
import json

from allauth.account.models import EmailAddress

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.signing import BadSignature, SignatureExpired
from django.core.validators import validate_email as _validate_email
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.views import generic
from django.urls import reverse
from django.utils.translation import gettext as _

from common import logging as log
from common.decorators import ajax_required
from users.auth import send_signup_link, signer, send_change_email_link
from users.forms import (
    SignupForm,
    UpdateUserForm,
    UserProfileForm,
    validate_username as val_username,
)
from users.models import SignupToken, User, ChangeEmailToken


logger = logging.getLogger(__name__)


@log.logit_view
@ajax_required
def send_singup_email(request):
    """Send sing up email to a client with the link to the sign up form."""
    if request.method == "POST":
        email = json.load(request).get("email")
        try:
            _validate_email(email)
        except ValidationError:
            return JsonResponse({"msg": "invalid"}, status=200)
        else:
            if send_signup_link(email):
                return JsonResponse({"msg": "sent"}, status=200)
    return JsonResponse({"msg": "error"}, status=200)


@log.logit_view
@ajax_required
def send_change_email(request):
    """Send change email message to a client with the link to the change view."""
    if request.method == "POST":
        email = json.load(request).get("email")
        try:
            _validate_email(email)
        except ValidationError:
            return JsonResponse({"msg": "invalid"}, status=200)
        else:
            if send_change_email_link(email):
                return JsonResponse({"msg": "sent"}, status=200)
    return JsonResponse({"msg": "error"}, status=200)


@log.logit_view
@login_required
def change_email(request, token):

    try:
        token = ChangeEmailToken.objects.get(token=token)
    except ChangeEmailToken.DoesNotExist:
        messages.add_message(
            request,
            messages.WARNING,
            _("You already changed email. If you didn't, make request again!"),
        )
        return redirect(reverse("content:home"))

    try:
        email = signer.unsign(token.token, max_age=7200)
    except SignatureExpired:
        return render(
            request,
            "error.html",
            {"message": "Signature Expired", "title": "Signature Expired"},
        )
    except BadSignature:
        return render(
            request,
            "error.html",
            {"message": "Bad Signature", "title": "Bad Signature"},
        )
    finally:
        logger.warning(
            log.VIEW_LOG_TEMPLATE.format(
                name=change_email.__name__,
                user=request.user,
                method=request.method,
                path=request.path,
            )
            + f"User have problems with changing email signature: token id {token.pk}"
        )
    if EmailAddress.objetcs.filter(email=email).exists():
        messages.add_message(
            request, messages.WARNING, _("You can't change your email.")
        )
        return redirect(reverse("content:home"))
    request.user.email = email
    request.user.save()
    messages.add_message(
        request, messages.INFO, _("The email successfully changed.")
    )
    token.delete()
    return redirect(reverse("content:home"))


@log.logit_view
@ajax_required
def validate_email(request):
    """Check if a user with a given email already exists in the database."""
    if request.method == "GET":
        email = request.GET.get("email", None)
        response = {
            "is_taken": EmailAddress.objects.filter(email=email).exists()
            or User.objects.filter(email=email).exists()
        }
        return JsonResponse(response, status=200)
    return JsonResponse({"is_taken": "error"}, status=200)


@log.logit_view
@ajax_required
def validate_username(request):
    """Check if a user with a given username already exists in the database."""
    if request.method == "GET":
        username = request.GET.get("username", None)
        try:
            if isinstance(username, str):
                username = "@" + username
                val_username(username)
        except ValidationError as e:
            return JsonResponse({"invalid": str(e.message)}, status=200)
        else:
            response = {
                "is_taken": User.objects.filter(username=username).exists()
                and not username == request.user.username
            }
        return JsonResponse(response, status=200)
    return JsonResponse({"is_taken": "error"}, status=200)


@log.logit_view
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
        token = SignupToken.objects.get(token=token)
    except SignupToken.DoesNotExist:
        messages.add_message(
            request,
            messages.WARNING,
            _(
                "You already registered. If you didn't register, request \
             for another link!"
            ),
        )
        return redirect(reverse("content:home"))

    try:
        email = signer.unsign(token.token, max_age=7200)
    except SignatureExpired:
        return render(request, template_name, {"error": "Signature Expired"})
    except BadSignature:
        return render(request, template_name, {"error": "Bad Signature"})
    finally:
        logger.warning(
            log.VIEW_LOG_TEMPLATE.format(
                name=signup.__name__,
                user=request.user,
                method=request.method,
                path=request.path,
            )
            + f"User have problems with sign up signature: token id {token.pk}"
        )

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


@log.logit_view
@ajax_required
def signin(request):
    """Sign in a user via ajax request."""
    if request.method == "POST":
        data = json.load(request)
        email = data.get("email")
        password = data.get("password")
        if not User.objects.filter(email=email).exists():
            return JsonResponse(
                {
                    "code": "noemail",
                    "error_message": _(
                        "Sorry, but we could not find a user account with \
                            that email."
                    ),
                }
            )
        user = authenticate(email=email, password=password)
        if not user:
            return JsonResponse(
                {
                    "code": "badpass",
                    "error_message": _("You have entered the wrong password."),
                }
            )
        login(
            request, user, backend="django.contrib.auth.backends.ModelBackend"
        )
        # TODO: redirect on referer
        return JsonResponse(
            {
                "code": "success",
                "redirect_url": reverse("content:home"),
            }
        )
    return HttpResponseBadRequest()


@log.logit_view
def signout(request):
    logout(request)
    return redirect(reverse("content:home"))


class UpdateUserProfile(LoginRequiredMixin, generic.TemplateView):
    template_name = "users/profile_settings.html"

    @log.logit_generic_view_request
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

    @log.logit_generic_view_request
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
