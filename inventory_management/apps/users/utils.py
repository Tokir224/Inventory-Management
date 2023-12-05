from django.core.mail import EmailMessage

from inventory_management.settings import settings


def send_email(subject, message, to_email):
    try:
        email_from = settings.EMAIL_HOST_USER
        mail = EmailMessage(subject, message, email_from, to=[to_email])
        mail.content_subtype = "html"
        mail.send()
        response = 1
    except Exception as e:
        response = 0
        print(e)
    return response


