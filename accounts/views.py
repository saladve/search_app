from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from .forms import SignupForm, LoginForm

class Signupview(CreateView):
    model = User
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('search_app:search')
    
    
class Loginview(LoginView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('search_app:search')


class Logoutview(LogoutView, LoginRequiredMixin):
    next_page = 'search_app/search.html'