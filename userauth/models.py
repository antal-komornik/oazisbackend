# from django.db import models
# from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
# phone = models.CharField(max_length=15, blank=True)
# address = models.TextField(blank=True)
# preferences = models.JSONField(default=dict)

#     def __str__(self):
#         return self.email


from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, default='')
    phone_number = models.CharField(max_length=20, blank=True, default='')

    def __str__(self):
        return self.user.username
