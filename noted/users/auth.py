"""Authentication, Authorization, Registration functions and utilities.

"""
import smtplib

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.signing import TimestampSigner
from django.utils.translation import gettext as _

from core import settings
from users.models import SignupToken

signer = TimestampSigner()


def send_signup_link(email_to: str) -> bool:
    """Send email to client with link for registration.

    Sign client's email to create the token for registration, send an email
    to the client with token and save the token to the database.

    Args:
        email_to: a client email.
    Returns:
        Success or failure ending boolean flag.
    """
    protocol = settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL
    if settings.ALLOWED_HOSTS:
        host = protocol + "://" + settings.ALLOWED_HOSTS[0]
    else:
        host = protocol + "://localhost:8000"
    token = signer.sign(email_to)
    context = {"host": host, "token": token}
    subject = _("Finish creating your account on NoteD.")
    email_from = settings.DEFAULT_FROM_EMAIL
    text_content = render_to_string("emails/signup_email.txt", context)
    html_content = render_to_string("emails/signup_email.html", context)

    try:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=email_from,
            to=[email_to],
            reply_to=[email_from],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        SignupToken.objects.create(token=token)
        return True
    except smtplib.SMTPException as e:
        print("There was an error sending an email: ", e)
        return False