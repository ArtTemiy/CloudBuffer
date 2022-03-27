import json
import os

from django.db import models
from jsonschema import validate as validate_json

from Accounts.models import Account
from CloudBuffer import config
from Files.models.schemas_storage import get_file_validation_schema
from Files.utils.token_generator import token_generator
from Files.utils.utils import get_file_path


class File(models.Model):
    # data types
    TEXT_TYPE = 'text'
    FILE_TYPE = 'file'
    _DATA_TYPES = [
        (TEXT_TYPE, 'text'),
        (FILE_TYPE, 'file'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    expire = models.DateTimeField()
    token = models.CharField(max_length=64)
    type = models.CharField(max_length=4, choices=_DATA_TYPES)
    metadata = models.CharField(max_length=2048, null=True)

    def get_file_path(self):
        return get_file_path(self.account, self.token)

    def validate(self):
        schema = get_file_validation_schema(self.type)
        validate_json(instance=json.loads(self.metadata), schema=schema)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.validate()
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        if os.path.exists(self.get_file_path()):
            os.remove(self.get_file_path())
        token_generator.remove_code(self.token)
        super().delete(using=using, keep_parents=keep_parents)


def clear_expired_files(account):
    while File.objects.filter(account=account).count() > config.MAX_FILES:
        file_to_clear = File.objects.filter(account=account).order_by('expire').first()
        print(f'file to clear: {file_to_clear.get_file_path()}')
        file_to_clear.delete()
