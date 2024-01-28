from django.db import models

# Create your models here.

class Gift(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    coin_price = models.PositiveIntegerField()

    def __str__(self):
        return self.name