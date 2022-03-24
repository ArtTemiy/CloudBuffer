from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import View

from Files.models import File
from utils.views_helpers import get_account


class FileApiView(LoginRequiredMixin, View):
    def get(self, request):
        pass

    def post(self, request):
        account = get_account(request)
        file = File.objects.filter(account=account).order_by('-expire').first()

        return HttpResponse(file.file.read())
