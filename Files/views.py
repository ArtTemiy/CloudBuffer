import datetime
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import View
from django.http.response import HttpResponseBadRequest, HttpResponse, HttpResponseNotFound, FileResponse

from Accounts.models import Account
from .models import File
from .forms import FileLoadForm
from .utils import gen_code
from utils.views_helpers import render_class_view_method, get_account, context_wrap

import CloudBuffer.config as config
import CloudBuffer.settings as settings
import redis


redis_cli = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class FileView(View):
    def get(self, request):
        return HttpResponseBadRequest()

    def post(self, request):
        return HttpResponseBadRequest()


class FileQRCode(View):
    def get(self, request):
        token = request.GET['token']
        print(f'token is {token}')

        file_id = redis_cli.get(token)
        print(f'file id is {file_id}')
        if not file_id:
            return HttpResponseBadRequest()
        file = File.objects.get(pk=file_id)
        if file.expire < timezone.now():
            return HttpResponseBadRequest()
        print(file.file.read())
        return FileResponse(open(file.file.path, 'rb'))


class FileLoadView(LoginRequiredMixin, View):
    get_func = render_class_view_method('files/file-load.html', {})

    def get(self, request):
        return self.get_func(request)

    def post(self, request):
        form = FileLoadForm(request.POST, request.FILES)
        print(request.POST, request.FILES)
        print(form.is_valid(), form.errors)
        if not form.is_valid():
            return HttpResponseBadRequest(form.errors)

        # get account
        file = request.FILES['file']
        account = get_account(request)

        # create file ()
        new_file = File(account=account, expire=datetime.datetime.now() + config.EXPIRE_TIME)
        new_file.save()

        # get file data
        file_content = file.read()

        # generate token
        token = gen_code()

        # TODO make it unique to allow several files with same names
        file_name = f'{token}__{file.name}'

        print(f'file was saved in path {file_name} with size {len(file_content)}b')

        # save file
        '''new_file.file.save(file_name, ContentFile(file_content))'''

        # clear old files
        '''while File.objects.filter(account=account).count() > config.MAX_FILES:
            file_to_clear = File.objects.filter(account=account).order_by('expire').first()
            print(f'file to clear: {file_to_clear.file.path}')
            file_to_clear.delete()
        file_id = new_file.pk'''

        print(new_file.file.path, new_file.file.read())

        # save token to redis
        while redis_cli.exists(token):
            token = gen_code()
        redis_cli.set(token, new_file.pk, config.EXPIRE_TIME.seconds)

        return render(request, 'files/file-qr.html', context_wrap(request, {
            'Title': 'File QR-code',
            'file_id': file_id,
            'token': token,
            'site_url': settings.ENDPOINT
        }))
