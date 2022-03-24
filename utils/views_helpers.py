from django.shortcuts import render
from django.views.decorators.http import require_GET

from Accounts.models import Account


def context_wrap(request, context):
    username = request.user.username
    context['username'] = username
    return context


def render_view(template_path, context):
    @require_GET
    def view_func(request):
        username = request.user.username
        context['username'] = username
        return render(request, template_path, context_wrap(request, context))

    return view_func


def render_class_view_method(template_path, context):
    def view_func(self, request):
        return render(request, template_path, context_wrap(request, context))

    return view_func


def get_account(request):
    return Account.objects.filter(user=request.user).first()
