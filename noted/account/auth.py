import smtplib

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.signing import Signer

from core import settings


signer = Signer()


def send_signup_link(email_to):
    protocol = settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL
    if settings.ALLOWED_HOSTS:
        host = protocol + '://' + settings.ALLOWED_HOSTS[0]
    else:
        host = protocol + '://localhost:8000'
    context = {'host': host, 'sign': signer.sign(email_to)}
    subject = 'Finish creating your account on NoteD.'
    email_from = settings.DEFAULT_FROM_EMAIL
    text_content = render_to_string('emails/signup_email.txt', context)
    html_content = render_to_string('emails/signup_email.html', context)

    try:
        msg = EmailMultiAlternatives(subject=subject, body=text_content,
            from_email=email_from, to=[email_to,], reply_to=[email_from,])
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)
        return True
    except smtplib.SMTPException as e:
        print('There was an error sending an email: ', e) 
        return False
