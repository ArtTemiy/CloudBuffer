import datetime
import json

import redis
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import FileResponse, JsonResponse
from django.views import View

import CloudBuffer.config as config
import CloudBuffer.settings as settings
from Files.models.models import File, clear_expired_files
from Files.utils.utils import get_file_path
from utils.views_helpers import get_account

redis_cli = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class BufferView(LoginRequiredMixin, View):
    # DATA_TYPE_HEADER = 'X-Data-Type'
    DATA_TYPE_HEADER = 'X_DATA_TYPE'
    HEADER_FILE_TYPES_BINDINGS = {
        'file': File.FILE_TYPE,
        'text': File.TEXT_TYPE,
    }
    FILE_TYPES_BINDINGS = {
        file_type: header
        for (header, file_type) in HEADER_FILE_TYPES_BINDINGS.items()
    }
    TOKEN = "@"

    def post(self, request):
        # checks request
        request_files_num = len(request.FILES)
        if request_files_num != 1:
            return JsonResponse({
                'error': 0,
                'message': f'Wrong number of files: {request_files_num}'
            }, status=400)
        data_type_header = request.headers.get(self.DATA_TYPE_HEADER, None)
        if data_type_header not in self.HEADER_FILE_TYPES_BINDINGS.keys():
            return JsonResponse({
                'error': 1,
                'message': f'Wrong data type header: {data_type_header}'
            }, status=400)

        account = get_account(request)

        old_file_obj = File.objects.filter(account=account, token=self.TOKEN).first()

        request_file = request.FILES['file']
        data = request_file.read()  # content
        # token = token_generator.gen_code()
        token = self.TOKEN
        file_path = get_file_path(account, token)
        file = open(file_path, 'wb+')
        file.write(data)
        file.close()

        metadata = {}
        data_type = self.HEADER_FILE_TYPES_BINDINGS[data_type_header]
        if data_type == File.FILE_TYPE:
            metadata = {
                'filename': request_file.name
            }
        else:
            pass

        if old_file_obj:
            old_file_obj.delete()

        new_file = File(
            account=account,
            expire=datetime.datetime.now() + config.EXPIRE_TIME,
            token=token,
            type=data_type,
            metadata=json.dumps(metadata),
        )
        new_file.save()
        print(f'file was saved in path {file_path} with size {len(data)}b')
        # file_id = new_file.pk
        # redis_cli.set(token, new_file.pk, config.EXPIRE_TIME.seconds)

        clear_expired_files(account)

        return JsonResponse({
            'code': 0,
            'message': 'ok'
        }, status=200)

    def get(self, request):
        account = get_account(request)

        token = self.TOKEN
        file_db_object = File.objects.get(account=account, token=token)
        filename = ''

        data_type = file_db_object.type
        data_type_header = self.FILE_TYPES_BINDINGS[data_type]

        if data_type_header != File.FILE_TYPE:
            filename = json.loads(file_db_object.metadata)['filename']
        elif data_type_header != File.TEXT_TYPE:
            pass
        return FileResponse(
            open(file_db_object.get_file_path(), 'rb'),
            filename=filename,
            headers={
                self.DATA_TYPE_HEADER: data_type_header
            }
        )
