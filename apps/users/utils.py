from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from rest_framework.reverse import reverse
from django.conf import settings


def send_activation_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_link = f"{reverse('users:user-activate', request=request)}?uid={uid}&token={token}"
    subject = "Activate your account"
    message = f"Hello {user.email},\nPlease activate your account using the link below:\n{activation_link}"

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
