"""Authentication, Authorization, Registration functions and utilities.

"""
import logging
import smtplib

from django.core.mail import EmailMultiAlternatives
from django.core.signing import TimestampSigner
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

from common.logging import logit
from core import settings

from .models import ChangeEmailToken, SignupToken


signer = TimestampSigner()
logger = logging.getLogger("emails")


@logit
def get_host() -> str:
    """Gets current host (schema + domain)."""
    protocol = settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL
    if "localhost" in settings.ALLOWED_HOSTS:
        return protocol + "://localhost:8000"
    else:
        return protocol + "://" + settings.ALLOWED_HOSTS[0]


@logit
def send_email(
    email_to: str, email_from: str, subject: str, text: str, html: str = ""
) -> bool:
    """Sends email to an user.

    Args:
        email_to: where to send a letter.
        email_from: from whom the letter will be sent.
        subject: a letter subject.
        text: a plain/text of the letter.
        html: html version of the letter.
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


@logit
def send_signup_link(email_to: str) -> bool:
    """Sends email to client with link for registration.

    Sign client's email to create the token for registration, send an email
    to the client with token and save the token to the database.

    Args:
        email_to: a client email.
    Returns:
        Success or failure ending boolean flag.
    """
    token = signer.sign(email_to)
    context = {"host": get_host(), "token": token}
    subject = _("Finish creating your account on NoteD.")
    email_from = settings.DEFAULT_FROM_EMAIL
    text_content = render_to_string("emails/signup_email.txt", context)
    html_content = render_to_string("emails/signup_email.html", context)

    if send_email(
        email_to, email_from, subject, text_content, html=html_content
    ):
        SignupToken.objects.create(token=token)
        return True
    return False


@logit
def send_change_email_link(email_to: str) -> bool:
    """Sends email to client with link for changing email.

    Sign client's email to create the token for changing, send an email
    to the client with token and save the token to the database.

    Args:
        email_to: a client email.
    Returns:
        Success or failure ending boolean flag.
    """
    token = signer.sign(email_to)
    context = {"host": get_host(), "token": token}
    if send_email(
        email_to,
        settings.DEFAULT_FROM_EMAIL,
        _("Finish changing your email on NoteD."),
        render_to_string("emails/change_email.txt", context),
        html=render_to_string("emails/change_email.html", context),
    ):
        ChangeEmailToken.objects.create(token=token)
        return True
    return False
