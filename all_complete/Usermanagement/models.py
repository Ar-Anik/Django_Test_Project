from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model) :
    picture = models.ImageField(upload_to='image/', blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    contact_num = models.CharField(max_length=200, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    