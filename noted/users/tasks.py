from celery import shared_task

from .auth import send_signup_email, send_changeemail_email


@shared_task()
def send_signup_email_task(email: str) -> bool:
    """Asynchronously sends a sign-up email to the specified email address.

    Args:
        email: The email address to send the sign-up email to.

    Returns:
        True if the email was sent successfully, otherwise False.
    """
    return send_signup_email(email)


@shared_task()
def send_changeemail_email_task(email: str) -> bool:
    """Asynchronously sends a change-email email to the specified email address.

    Args:
        email: The email address to send the change-email email to.

    Returns:
        True if the email was sent successfully, otherwise False.
    """
    return send_changeemail_email(email)
