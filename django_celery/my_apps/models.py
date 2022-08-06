from celery.app import shared_task
from django.db import models
import os 


# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=2083, default="", unique=True)
    published = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    source = models.CharField(max_length=30, default="", blank=True, null=True)

    def __ster__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=100)
    mv_original = models.FileField(null=True,blank=True, upload_to='movies/')
    audio = models.FileField(null=True, blank=True, upload_to='movies/')

    def __str__(self):
        return self.title

    
    def filename(self):
        name = os.path.basename(self.mv_original.name)
        return name.split('.')[0]
