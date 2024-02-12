from django.db import models

# Create your models here.

class Gift(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    coin_price = models.PositiveIntegerField()
    image = models.ImageField(upload_to='gift/media/images/', default='gift/media/images/gift-box.png')

    def __str__(self):
        return self.name