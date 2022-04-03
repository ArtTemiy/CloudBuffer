import json

import redis
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import FileResponse, JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from jsonschema import ValidationError as JsonSchemaValidationError

import CloudBuffer.config as config
import CloudBuffer.settings as settings
from Files.models.models import File
from Files.utils.utils import get_file_path
from utils.views_helpers import get_account

redis_cli = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


@method_decorator(csrf_exempt, name='dispatch')
class BufferView(LoginRequiredMixin, View):
    DATA_TYPE_HEADER = 'X-Data-Type'
    HEADER_FILE_TYPES_BINDINGS = {
        'file': File.FILE_TYPE,
        'text': File.TEXT_TYPE,
    }
    FILE_TYPES_BINDINGS = {
        file_type: header
        for (header, file_type) in HEADER_FILE_TYPES_BINDINGS.items()
    }
    TOKEN = "@"

    @method_decorator(csrf_exempt)
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

        request_file = request.FILES['file']
        request_filename = request_file.name
        token = self.TOKEN
        data = request_file.read()  # content
        file_path = get_file_path(account, token)

        metadata = {}
        data_type = self.HEADER_FILE_TYPES_BINDINGS[data_type_header]
        if data_type == File.FILE_TYPE:
            metadata = {
                'filename': request_filename
            }
        else:
            pass
        new_file = File(
            account=account,
            expire=timezone.now() + config.EXPIRE_TIME,
            token=token,
            type=data_type,
            metadata=json.dumps(metadata),
        )
        try:
            new_file.validate()
        except JsonSchemaValidationError as e:
            return JsonResponse({
                'code': 1,
                'message': f'error while validating: {e}'
            }, status=400)

        old_file_obj = File.objects.filter(account=account, token=self.TOKEN).first()
        if old_file_obj:
            old_file_obj.delete(delete_file=False)

        file = open(file_path, 'wb+')
        file.write(data)
        file.close()

        new_file.save()
        print(f'file was saved in path {file_path} with size {len(data)}b')

        return JsonResponse({
            'code': 0,
            'message': 'ok'
        }, status=200)

    def get(self, request):
        account = get_account(request)

        token = self.TOKEN
        file_db_object = File.objects.filter(account=account, token=token).first()
        if file_db_object is None:
            return JsonResponse({
                'code': 0,
                'message': f'no data in buffer for user {account.user.username}'
            }, status=404)
        filename = ''

        data_type = file_db_object.type
        data_type_header = self.FILE_TYPES_BINDINGS[data_type]

        if data_type_header == File.FILE_TYPE:
            filename = json.loads(file_db_object.metadata)['filename']
        elif data_type_header == File.TEXT_TYPE:
            pass
        return FileResponse(
            open(file_db_object.get_file_path(), 'rb'),
            filename=filename,
            as_attachment=True,
            headers={
                self.DATA_TYPE_HEADER: data_type_header
            }
        )
