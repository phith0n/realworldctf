from django.db import models
from django.utils import timezone
from django.conf import settings


class Image(models.Model):
    path = models.FilePathField('img path')

    created_time = models.DateTimeField('创建时间', default=timezone.now)
    last_modify_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        ordering = ['-created_time']
        verbose_name = "image path"
        verbose_name_plural = "image paths"

    def __str__(self):
        return str(self.path)

    def get_absolute_url(self):
        return f'{settings.MEDIA_URL}{self.path}'
