from django.db import models
from django.contrib.auth.models import User

class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.name