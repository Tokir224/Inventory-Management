from django.template.loader import get_template
from .utils import send_email
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .models import Users
from django.contrib.auth.tokens import default_token_generator


def set_password_link_mail(activation_link, to_email, user_id):
    user = Users.objects.filter(id=user_id).first()
    context = {
        'activation_link': activation_link,
        'user': user,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'token': default_token_generator.make_token(user),
    }

    mail_subject = 'Reset Password Link'

    mail_message = get_template('profile/password_reset_email.html').render(context)
    send_email(mail_subject, mail_message, to_email)


def credential_mail(activation_link, email, password):
    context = {
        'activation_link': activation_link,
        'email': email,
        'password': password,
    }

    mail_subject = 'Your account has been created'

    mail_message = get_template('profile/credential.html').render(context)
    send_email(mail_subject, mail_message, email)
