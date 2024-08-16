from django.db import models


class Note(models.Model):
    status = models.BooleanField(default=False)
    text = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заметка'

