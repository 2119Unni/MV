from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery', blank=True)

    class Meta:
        ordering = ('name',)

    def get_url(self):
        return reverse('MovieApp:product_by_category', args=[self.slug])

    # product_by_category = Category list URl name

    def __str__(self):
        return '{}'.format(self.name)


class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    desc = models.TextField(null=True, blank=True)
    year = models.IntegerField(blank=True)
    img = models.ImageField(blank=True, default='media/gallery/Empty.png', upload_to='gallery')

    def __str__(self):
        return self.name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=100)
    review = models.TextField(null=True, blank=True)
    movie = models.ForeignKey(Movie, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.caption
