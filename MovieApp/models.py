from django.contrib.auth.models import User
from django.db import models
# Create your models here.
class Movie(models.Model):
    user = models.CharField(max_length=250, null=True)
    name = models.CharField(max_length=250)
    desc = models.TextField(null=True, blank=True)
    year = models.IntegerField(blank=True)
    img = models.ImageField(blank=True,default='media/gallery/Empty.png',upload_to='gallery')
    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=100)
    review = models.TextField(null=True, blank=True)
    movie = models.ForeignKey(Movie,null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption