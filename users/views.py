from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import CommonMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(CommonMixin, LoginView):
    """View for handling user login."""
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Shop - Authorization'


class UserRegistrationView(CommonMixin, SuccessMessageMixin, CreateView):
    """View for handling user registration."""
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Congratulations, you have successfully registered!'
    title = 'Shop - Registration'


class UserProfileView(CommonMixin, UpdateView):
    """View for handling user profile update."""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Shop - Profile'

    # Redirect to user's profile page after successful update
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(CommonMixin, TemplateView):
    """View for handling email verification."""
    title = 'Store - Email confirmation'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            # Redirect to home page if email verification fails or is expired
            return HttpResponseRedirect(reverse('index'))
