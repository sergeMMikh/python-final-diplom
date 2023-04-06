# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import EmailMessage
# from rest_framework.authtoken.models import Token
from orders.tasks import send_email


def send_email_4_verification(current_site: str,
                              user_email: str,
                              token: str) -> None:
    message = f"Please follow this link to confirm your password: \n " \
              f"http://{current_site}/api/v1/user/verify_email/" \
              f"{token}"
    send_email.delay(title='Verify email',
                     message=message,
                     to=user_email)


def send_email_4_reset_passw(user_email: str,
                             token: str) -> None:
    message = f"Please use this token for you request : \n " \
              f"{token}"
    send_email.delay(title='reset_password',
                     message=message,
                     from_='django_app',
                     to=user_email)
