from django.db import models

# Create your models here.
class Articles(models.Model):
    image=models.ImageField()
    article=models.TextField()