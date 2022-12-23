import json

from allauth.account.models import EmailAddress

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ValidationError
from django.core.signing import BadSignature, SignatureExpired
from django.core.validators import validate_email as _validate_email
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from users.auth import send_signup_link, signer
from users.forms import SignupForm
from users.models import SignupToken, User
from common.decorators import ajax_required
from common.logging import logging_view


@logging_view
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
            success = send_signup_link(email)
            if success:
                return JsonResponse({"msg": "sent"}, status=200)
    return JsonResponse({"msg": "error"}, status=200)


@logging_view
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


@logging_view
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
            return redirect(reverse("content:home"))
        else:
            context["form"] = form
            return render(request, template_name, context)


@logging_view
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


@logging_view
def signout(request):
    logout(request)
    return redirect(reverse("content:home"))
