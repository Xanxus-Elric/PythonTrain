from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Issue(models.Model):
    EIP = models.CharField(max_length=100)
    Auth = models.ForeignKey(User, default="Edward", related_name="Engineer", on_delete=models.CASCADE)
    Desc = models.TextField()
    Publish = models.DateTimeField(default=timezone.now)

    #re-define the embeded class
    class Meta:
        ordering = ("Publish", )


