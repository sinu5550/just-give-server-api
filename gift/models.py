from django.db import models

# Create your models here.

class Gift(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    coin_price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='book/images/', default='book/images/gift-box.png')

    def __str__(self):
        return self.name