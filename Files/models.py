from django.core.files import storage
import os
from django.db import models

from Accounts.models import Account
from CloudBuffer.settings import MEDIA_ROOT

import hashlib


class File(models.Model):
    # relative
    file_path = models.CharField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    expire = models.DateTimeField()

    def get_full_path(self):
        return MEDIA_ROOT + self.file_path

    def get_token(self):
        content = open(self.get_full_path(), 'r').read()
        username = self.account.user.username
        datetime = self.expire.strftime('%c')

        file_hash = \
            int(hashlib.sha256(content).hexdigest(), 16) ^ \
            int(hashlib.sha256(username).hexdigest(), 16) ^ \
            int(hashlib.sha256(datetime).hexdigest(), 16) ^ \
            int(hashlib.sha256(self.pk).hexdigest(), 16)
        file_hash_string = hex(file_hash)[2:]

        return file_hash_string

    def delete(self, using=None, keep_parents=False):
        if os.path.exists(self.get_full_path()):
            os.remove(self.get_full_path())
        super().delete(using=using, keep_parents=keep_parents)
