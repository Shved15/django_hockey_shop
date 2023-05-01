from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    # the fields check if the user has confirmed the mail
    is_verified_email = models.BooleanField(default=False)
    email = models.EmailField(unique=True)


class EmailVerification(models.Model):
    # field for generating a unique identifier
    code = models.UUIDField(unique=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    # field defines when the verification link expires
    expiration = models.DateTimeField()

    def __str__(self):
        return f'Email verification object for user - {self.user.username} | {self.user.email}'

    def send_verification_mail(self):
        link = reverse('users:email_verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = f'{self.user.username} account verification'
        message = 'To confirm the account for the {} follow the link {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    # check the validity of the verification link
    def is_expired(self):
        return True if now() >= self.expiration else False
