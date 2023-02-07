from django.conf import settings
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(default='pictures/default.png', upload_to='pictures/%Y/%m/%d')
    created = models.DateField(null=True, auto_now_add=True, blank=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"Profile for user {self.user.username}"
