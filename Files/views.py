import datetime
import json

import redis
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseBadRequest, FileResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

import CloudBuffer.config as config
import CloudBuffer.settings as settings
from Files.models.models import File
from Files.utils.token_generator import token_generator
from Files.utils.utils import get_file_path
from utils.views_helpers import render_class_view_method, get_account, context_wrap
from .forms import FileLoadForm

redis_cli = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class FileView(View):
    def get(self, request):
        return HttpResponseBadRequest()

    def post(self, request):
        return HttpResponseBadRequest()


class FileGet(View):
    def get(self, request):
        token = request.GET['token']
        print(f'token is {token}')

        file_id = redis_cli.get(token)
        print(f'file id is {file_id}')
        if not file_id:
            return HttpResponseBadRequest()
        file_db_object = File.objects.get(pk=file_id)
        if file_db_object.expire < timezone.now():
            file_db_object.delete()
            return HttpResponseBadRequest()
        print(file_db_object.get_file_path())
        if file_db_object.type != file_db_object.FILE_TYPE:
            return HttpResponseBadRequest()

        filename = json.loads(file_db_object.metadata)['filename']
        return FileResponse(open(file_db_object.get_file_path(), 'rb'), filename=filename)


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
        request_file = request.FILES['file']
        account = get_account(request)

        # get file data
        file_content = request_file.read()

        # generate token
        token = token_generator.gen_code()
        file_path = get_file_path(account, token)
        # file_path = f'{account.user.username}__{file.name}__{token}'
        file = open(file_path, 'wb+')
        file.write(file_content)
        file.close()

        # create file object in db
        new_file = File(
            account=account,
            expire=datetime.datetime.now() + config.EXPIRE_TIME,
            token=token,
            type=File.FILE_TYPE,
            metadata=json.dumps({
                'filename': request_file.name
            }),
        )
        new_file.save()

        print(f'file was saved in path {file_path} with size {len(file_content)}b')

        # clear old files
        while File.objects.filter(account=account).count() > config.MAX_FILES:
            file_to_clear = File.objects.filter(account=account).order_by('expire').first()
            print(f'file to clear: {file_to_clear.get_file_path()}')
            file_to_clear.delete()
        file_id = new_file.pk

        print(new_file.get_file_path())

        # save token to redis
        redis_cli.set(token, new_file.pk, config.EXPIRE_TIME.seconds)

        return render(request, 'files/file-get.html', context_wrap(request, {
            'Title': 'File QR-code',
            'file_id': file_id,
            'token': token,
            'site_url': settings.ENDPOINT
        }))
