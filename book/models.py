from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Book(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return f"{self.title} - posted by - {self.user}"