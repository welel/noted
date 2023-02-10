"""Authentication, Authorization, Registration functions and utilities.

"""
import logging
import smtplib
from typing import Literal, NamedTuple, Optional

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from common.logging import LogMessage

from .models import AuthToken


MESSAGES = {
    "su_token_miss": _(
        "You already registered or the URL link is invalid."
        " If you didn't register, request for another link!"
    ),
    "ce_token_miss": _(
        "You already changed email or the URL link is invalid."
        " If you didn't, make request again!"
    ),
    "signed_social": _(
        "You can't change your email because you signed up via"
        " a third paty service."
    ),
    "email_changed": _("The email was successfully changed."),
    "noemail": _(
        "Sorry, but we could not find a user account with that email."
    ),
    "wrong_pass": _("You have entered the wrong password."),
}


signer = TimestampSigner()
logger = logging.getLogger("emails")


class Email(NamedTuple):
    email: Optional[str] = None
    error: Optional[str] = None


class StringToken(NamedTuple):
    """String representation of a token."""

    token: str
    type: Literal["su", "cm"]


class TokenData(NamedTuple):
    token: Optional[AuthToken] = None
    email: Optional[str] = None
    error: Optional[str] = None


def get_host() -> str:
    """Gets current host (schema + domain)."""
    protocol = settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL
    if "localhost" in settings.ALLOWED_HOSTS:
        return protocol + "://localhost:8000"
    else:
        return protocol + "://" + settings.ALLOWED_HOSTS[0]


def send_email(
    email_to: str, email_from: str, subject: str, text: str, html: str = ""
) -> bool:
    """Sends email to an user.

    Args:
        email_to: Where to send a letter.
        email_from: From whom the letter will be sent.
        subject: A letter subject.
        text: A plain/text of the letter.
        html: HTML version of the letter.

    Returns:
        Success or failure ending boolean flag.
    """
    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text,
            from_email=email_from,
            to=[email_to],
            reply_to=[email_from],
        )
        if html:
            msg.attach_alternative(html, "text/html")
        msg.send(fail_silently=False)
        logger.info(
            "Sing up email sent to: {}\nSubject: {}".format(email_to, subject)
        )
        return True
    except smtplib.SMTPException as e:
        logger.error(
            "There was an error sending an email to {}: {}\nOn subject: {}".format(
                email_to, str(e), subject
            )
        )
        return False


def send_email_with_token(
    email_to: str,
    type: str,
    subject: str,
    text_content_path: str,
    html_content_path: str,
) -> bool:
    """Sends tokenized email to the client.

    Sign a client's email to create the token, send an email to the client
    with token and save the token to the database.

    Args:
        email_to: A client email.
        type: A type of a token.
        subject: A email subject.
        text_content_path: A relative path to the email plain/text template.
        html_content_path: A relative path to the email plain/html template.

    Returns:
        Success or failure ending boolean flag.
    """
    token = signer.sign(email_to)
    context = {"host": get_host(), "token": token}
    email_from = settings.DEFAULT_FROM_EMAIL
    text_content = render_to_string(text_content_path, context)
    html_content = render_to_string(html_content_path, context)

    if send_email(
        email_to, email_from, subject, text_content, html=html_content
    ):
        _, created = AuthToken.objects.get_or_create(token=token, type=type)
        return created
    return False


def send_signup_email(email_to: str) -> bool:
    """Sends email to client with link for registration.

    Args:
        email_to: A client email.

    Returns:
        Success or failure ending boolean flag.
    """
    subject = _("Finish creating your account on NoteD.")
    text_content_path = "emails/signup_email.txt"
    html_content_path = "emails/signup_email.html"
    return send_email_with_token(
        email_to,
        AuthToken.SIGNUP,
        subject,
        text_content_path,
        html_content_path,
    )


def send_changeemail_email(email_to: str) -> bool:
    """Sends email to client with link for changing email.

    Args:
        email_to: A client email.

    Returns:
        Success or failure ending boolean flag.
    """
    subject = _("Finish changing your email on NoteD.")
    text_content_path = "emails/change_email.txt"
    html_content_path = "emails/change_email.html"
    return send_email_with_token(
        email_to,
        AuthToken.CHANGE_EMAIL,
        subject,
        text_content_path,
        html_content_path,
    )


def get_token(token: StringToken) -> Optional[AuthToken]:
    """Returns :model:`AuthToken` instance if exists, `None` otherwise."""
    try:
        return AuthToken.get_from_str(token=token.token, type=token.type)
    except AuthToken.DoesNotExist:
        return None


def unsign_email(token: AuthToken) -> Email:
    """Converts a signed email (token) to the email address using the signer.

    Args:
        token: a :model:`AuthToken` instance to unsign.

    Returns:
        A email named tuple with email and error message.
    """
    try:
        email = signer.unsign(token.token, max_age=7200)
    except SignatureExpired:
        return Email(error=_("Signature Expired"))
    except BadSignature as error:
        log_message = LogMessage(error, unsign_email, token)
        logger.error(
            f"User have problems with changing email signature: token id {token.pk}\n"
            + str(log_message)
        )
        return Email(error=_("Bad Signature"))
    return Email(email=email)
