from django.db import models
from django.forms import ModelForm


# Create your models here
class Result(models.Model):
    data = models.TextField(default="Null")
    author = models.CharField(max_length=200, default="Null")

    def __str__(self):
        return self.data

