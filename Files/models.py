import hashlib
import os

from django.db import models

from Accounts.models import Account


class File(models.Model):
    file_path = models.CharField(max_length=1024, null=False)
    file_name = models.CharField(max_length=1024, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    expire = models.DateTimeField()

    def get_token(self):
        content = open(self.file_path, 'r').read()
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
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        super().delete(using=using, keep_parents=keep_parents)
