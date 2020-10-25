from django.db import models
from django.contrib.auth.models import User
from pathlib import Path
from django.conf import settings
import os

def user_directory_path(instance, filename):
    return 'account_image/{0}{1}'.format(instance.user.username, Path(filename).suffix)


class InfoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Аватарка', upload_to=user_directory_path, blank=True,
                              default="default/default.jpg")

    class Meta:
        verbose_name = 'Аватарка'
        verbose_name_plural = 'Аватарки'

    def __str__(self):
        return self.user.username
