from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    User = get_user_model()

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE
                                )
    name = models.CharField(max_length=100,
                            null=True,
                            blank=True
                            )
    surname = models.CharField(max_length=100,
                               null=True,
                               blank=True
                               )
    created_at = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars',
                               null=True,
                               blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.user.username
