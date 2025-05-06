from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from jwt.utils import force_bytes

from instory import settings
from users.backends import User
from users.utils import EmailVerificationTokenGenerator


def send_verification_email(user: User):
    uidb64 = urlsafe_base64_encode(force_bytes(str(user.pk)))
    token = EmailVerificationTokenGenerator().make_token(user)
    url = f'{settings.FRONTEND_EMAIL_VERIFY_URL}/{uidb64}/{token}'

    email_subject = f'Verify your {settings.APP_NAME} account'
    email_body = render_to_string('emails/email-verification.html', {
        'user': user,
        'app_name': settings.APP_NAME,
        'app_url': settings.APP_URL,
        'verify_url': url,
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    email.content_subtype = "html"
    email.send()


def send_password_reset_email(user: User):
    uidb64 = urlsafe_base64_encode(force_bytes(str(user.pk)))
    token = PasswordResetTokenGenerator().make_token(user)
    url = f'{settings.FRONTEND_PASSWORD_RESET_URL}/{uidb64}/{token}'

    email_subject = f'Reset your {settings.APP_NAME} password'
    email_body = render_to_string('emails/password-reset.html', {
        'user': user,
        'app_name': settings.APP_NAME,
        'app_url': settings.APP_URL,
        'reset_url': url,
    })

    email = EmailMessage(subject=email_subject, body=email_body, from_email=settings.EMAIL_FROM_USER, to=[user.email])
    email.content_subtype = "html"
    email.send()
