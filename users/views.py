from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView

from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm

from products.models import Bag
from users.models import User


# create class-controller for authentication and authorization
class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


# class controller for creation new user
class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super(UserRegistrationView, self).get_context_data()
        context['title'] = 'Shop - Registration'
        return context


# class controller for profile of user
class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    # the same as 'HttpResponseRedirect(reverse('users:login'))', redirect to user's profile page
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['title'] = 'Shop - Profile'
        context['bags'] = Bag.objects.filter(user=self.object)
        return context

# controller-function for registration page
# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Congratulations, you have successfully registered!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/registration.html', context)


# controller-function for profile page
# login_required - the controller will not work until user logs in
# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#     context = {
#         'title': 'Store - Profile',
#         'form': form,
#         'bags': Bag.objects.filter(user=request.user)
#     }
#     return render(request, 'users/profile.html', context)
