from django.contrib.auth.models import User
from django.db import models


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(null=True, default=None)

    def __str__(self):
        return f'{self.pk}::{self.user.__str__()}'
