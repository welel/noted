from celery import shared_task

from .auth import send_signup_email, send_changeemail_email


@shared_task()
def send_signup_email_task(email: str) -> bool:
    return send_signup_email(email)


@shared_task()
def send_changeemail_email_task(email: str) -> bool:
    return send_changeemail_email(email)
