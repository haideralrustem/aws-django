from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Info(models.Model):

    section_title = models.CharField(max_length=250)
    section_text = models.TextField()

    date_posted = models.DateTimeField(default=timezone.now())

    author  = models.ForeignKey(User, on_delete=models.CASCADE)  # if user is deleted, info is deleted


    def __str__(self):
        return self.section_title

