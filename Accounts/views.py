from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import render
from django.views import View
from django.views.decorators.http import require_GET

from utils.views_helpers import render_view
from .forms import RegisterForm, LoginForm
from .models import Account


class RegisterView(View):
    def get(self, request):
        templates_args = {
            'title': 'Register'
        }
        return render(request, 'accounts/register.html', templates_args)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if len(User.objects.filter(username=data['username'])) > 0:
                # TODO - No content on frontend
                return HttpResponse('User already exists', status=400)
            new_user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=data['password']
            )
            new_account = Account(user=new_user)
            new_account.save()
            login(request, new_user)
            return HttpResponse('', status=200)
        else:
            print(form.errors)
            return HttpResponseBadRequest(form.errors)


class LogInView(View):
    def get(self, request):
        return render(request, 'accounts/login.html', {})

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            print(form.errors)
            return HttpResponseBadRequest(form.errors)
        data = form.cleaned_data
        if len(User.objects.filter(username=data['username'])) > 0:
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                login(request, user)
                return HttpResponse('', status=200)
            else:
                return HttpResponseForbidden()


class LogOutView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/logout.html', {
            'title': 'Log Out',
        })

    def post(self, request):
        logout(request)
        return render(request, 'accounts/logout-done.html')


@require_GET
@login_required
def profile_view(request):
    username = request.user.username
    return render(request, 'accounts/profile.html', {
        'title': 'Profile',
        'username': username,
        'user': request.user,
    })


login_done = render_view('accounts/login-done.html', {'title': 'Log In'})
logout_done = render_view('accounts/logout-done.html', {'title': 'Log Out'})
register_done = render_view('accounts/register-done.html', {'title': 'Register'})
